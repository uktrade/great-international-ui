import pytest
import re
from bs4 import BeautifulSoup
from django.template import Template, Context
from django.test import RequestFactory


@pytest.mark.parametrize('input_query_string,expected_query_string', (
        ('foo=bar&baz=1', 'foo=bar&amp;baz=1&amp;page=3'),
        ('foo=bar&baz=1&page=2', 'foo=bar&amp;baz=1&amp;page=3'),
        ('page=1', 'page=3'),
        ('', 'page=3'),
))
def test_update_query(input_query_string, expected_query_string):
    request_factory = RequestFactory()
    request = request_factory.get('/page-url?{}'.format(input_query_string))
    template = Template(
        '{% load update_query_params from atlas_tags %}'
        '{% update_query_params page=3 %}'
    )
    context = Context({'request': request})

    rendered = template.render(context)
    assert rendered == expected_query_string


@pytest.mark.parametrize('id, input, has_button, visible, collapsed', (
        ('id1', '<p>some text</p>', False, '<p>some text</p>', ''),  # Does not split if no <hr>
        ('id2', '<p>some text</p><hr><p>more text</p>', True, '<p>some text</p>', '<p>more text</p>'),  # Splits if <hr>
        ('id3', '<p>some text</p><hr>', False, '<p>some text</p>', ''),  # Does not split if no content after <hr>
        ('id4', '<p>some text</p><hr><p>more text</p><hr><p>even more text</p>', True, '<p>some text</p>',
         '<p>more text</p><hr/><p>even more text</p>'),  # Only splits first <hr>
        ('id5', '<p>some text</p><hr/><p>more text</p>', True, '<p>some text</p>', '<p>more text</p>'),
        # Splits if <hr/>
))
def test_collapsible_cms_text(id, input, has_button, visible, collapsed):
    template = Template(
        '{% load collapse_text from atlas_tags %}'
        '{% collapse_text input|safe id %}'
    )
    context = Context({'input': input, 'id': id})
    rendered = template.render(context)

    soup = BeautifulSoup(rendered, 'html.parser')
    button = soup('button')
    rendered_visible = soup.find(class_='atlas-collapsible__initial')
    rendered_collapsed = soup.find(class_='atlas-collapsible__content')

    assert bool(button) == has_button
    assert str(rendered_visible.decode_contents()).strip() == visible
    if has_button:
        assert button[0]['aria-controls'] == 'atlas-collapsible-{}'.format(id)
        assert str(rendered_collapsed.decode_contents()).strip() == collapsed


def test_cms_url(settings):
    settings.DIRECTORY_CMS_API_CLIENT_BASE_URL = 'http://example.org/cms-url'
    template = Template(
        '{% load cms_url from atlas_tags %}'
        '{% cms_url %}'
    )
    context = Context()
    rendered = template.render(context)

    assert 'http://example.org/cms-url' in rendered


@pytest.mark.parametrize('page_url, filter_name, chosen_filters, num_commas, shows_or, remove_urls', (
        # One filter -- no comma, no 'and'
        ("/page-url?foo=One", 'foo', ['One'], 0, False, ["/page-url"]),
        # Two filters -- no comma, 'and' present
        ("/page-url?foo=One&foo=Two", 'foo', ['One', 'Two'], 0, True, ["/page-url?foo=Two", "/page-url?foo=One"]),
        # Three filters -- one comma, 'and' present
        ("/?foo=One&foo=Two&foo=Three", 'foo', ['One', 'Two', 'Three'], 1, True,
         ["/?foo=Two&amp;foo=Three", "/?foo=One&amp;foo=Three", "/?foo=One&amp;foo=Two"]),
        # 5 filters -- 3 commas, 'and' present
        ("/?a=1&a=2&a=3&a=4&a=5", 'a', ['1', '2', '3', '4', '5'], 3, True,
         ["/?a=2&amp;a=3&amp;a=4&amp;a=5", "/?a=1&amp;a=3&amp;a=4&amp;a=5", "/?a=1&amp;a=2&amp;a=4&amp;a=5",
          "/?a=1&amp;a=2&amp;a=3&amp;a=5", "/?a=1&amp;a=2&amp;a=3&amp;a=4"]),
        # test other parameters are retained
        ("/?foo=One&bar=baz", 'foo', ['One'], 0, False, ["/?bar=baz"])

))
def test_chosen_filters_multiple(page_url, filter_name, chosen_filters, num_commas, shows_or, remove_urls):
    request_factory = RequestFactory()
    request = request_factory.get(page_url)
    template = Template(
        '{% load chosen_filters from atlas_tags %}'
        '{% chosen_filters filter_name chosen_filters %}'
    )
    context = Context({
        'filter_name': filter_name,
        'chosen_filters': chosen_filters,
        'request': request
    })
    rendered = template.render(context)

    for chosen_filter in chosen_filters:
        # Text node between tags
        assert re.search('>\\s*{}\\s*<'.format(chosen_filter), rendered)
    assert rendered.count(',') == num_commas
    if shows_or:
        assert ' and ' in rendered
    else:
        assert ' and ' not in rendered
    for url in remove_urls:
        assert '"{}"'.format(url) in rendered
