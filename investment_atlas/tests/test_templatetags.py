import pytest
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
