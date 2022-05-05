import pytest
import re
from bs4 import BeautifulSoup
from django.template import Template, Context
from django.test import RequestFactory


@pytest.mark.parametrize('query_string, arguments, expected', (
        ('?foo=bar&baz=1', 'page=3', '?foo=bar&amp;baz=1&amp;page=3'),
        ('?foo=bar&baz=1&page=2', 'page=3', '?foo=bar&amp;baz=1&amp;page=3'),
        ('?page=1', 'page=3', '?page=3'),
        ('', 'page=3', '?page=3'),
        ('?foo=bar', 'foo=""', ''),
        ('?foo=bar&page=2', 'foo=""', '?page=2'),
        ('?foo=bar&baz=1&page=2', 'foo=""', '?baz=1&amp;page=2'),
        ('?baz=two', 'foo=""', '?baz=two'),
))
def test_update_query(query_string, arguments, expected):
    request_factory = RequestFactory()
    request = request_factory.get('/page-url{}'.format(query_string))
    template = Template(
        '{{% load update_query_params from atlas_tags %}}{{% update_query_params {} %}}'.format(arguments))
    context = Context({'request': request})

    rendered = template.render(context)
    assert rendered == expected


@pytest.mark.parametrize('id, input, has_button, visible, collapsed', (
        # Does not split if no <hr>
        ('id1', '<p>some text</p>', False, '<p>some text</p>', ''),
        # Splits if <hr>
        ('id2', '<p>some text</p><hr><p>more text</p>', True, '<p>some text</p>', '<p>more text</p>'),
        # Does not split if no content after <hr>
        ('id3', '<p>some text</p><hr>', False, '<p>some text</p>', ''),
        # Only splits first <hr>
        ('id4', '<p>some text</p><hr><p>more text</p><hr><p>even more text</p>', True, '<p>some text</p>',
            '<p>more text</p><hr/><p>even more text</p>'),
        # Splits if <hr/>
        ('id5', '<p>some text</p><hr/><p>more text</p>', True, '<p>some text</p>', '<p>more text</p>'),
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


@pytest.mark.parametrize('page_url, filter_name, chosen_filters, shows_and, remove_urls', (
        # One filter
        ("/page-url?foo=One", 'foo', ['One'], False, ["/page-url"]),
        # Two filters
        ("/page-url?foo=One&foo=Two", 'foo', ['One', 'Two'], True, ["/page-url?foo=Two", "/page-url?foo=One"]),
        # Three filters
        ("/?foo=One&foo=Two&foo=Three", 'foo', ['One', 'Two', 'Three'], True,
            ["/?foo=Two&amp;foo=Three", "/?foo=One&amp;foo=Three", "/?foo=One&amp;foo=Two"]),
        # test other parameters are retained
        ("/?foo=One&bar=baz", 'foo', ['One'], False, ["/?bar=baz"])

))
def test_chosen_filters_multiple(page_url, filter_name, chosen_filters, shows_and, remove_urls):
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

    # Check the filter label is rendered
    for chosen_filter in chosen_filters:
        # Text node between tags
        assert re.search('>\\s*{}\\s*<'.format(chosen_filter), rendered)

    # Check whether 'and' is shown
    if shows_and:
        assert ' and ' in rendered
    else:
        assert ' and ' not in rendered

    # Check URLs
    for url in remove_urls:
        assert '"{}"'.format(url) in rendered


def test_chosen_filter_empty():
    request_factory = RequestFactory()
    request = request_factory.get("/?foo=bar")
    template = Template(
        '{% load chosen_filters from atlas_tags %}'
        '{% chosen_filters filter_name chosen_filters %}'
    )
    context = Context({
        'filter_name': 'bar',
        'chosen_filters': [],
        'request': request
    })
    rendered = template.render(context)

    assert rendered.strip() == ''
