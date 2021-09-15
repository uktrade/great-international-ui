import pytest
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
