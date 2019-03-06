import pytest
from core.templatetags import cms_tags


def test_prefix_path():
    actual = cms_tags.prefix_path('/article-list/article-slug/')
    expected = '/international/article-list/article-slug/'
    assert actual == expected


heading_types = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


@pytest.mark.parametrize('heading', heading_types)
def test_convert_headings_to(heading):
    actual = cms_tags.convert_headings_to(
        '<' + heading + '></' + heading + '>',
        'figure'
    )
    expected = '<figure></figure>'
    assert actual == expected


def test_convert_headings_to_does_not_convert_non_headings():
    actual = cms_tags.convert_headings_to('<span></span>', 'figure')
    expected = '<span></span>'
    assert actual == expected


def test_override_class_on_h2_elements():
    actual = cms_tags.override_class_on_h2_elements('<h2></h2>', 'test-class')
    expected = '<h2 class="test-class"></h2>'
    assert actual == expected


def test_override_class_on_h4_elements():
    actual = cms_tags.override_class_on_h4_elements('<h4></h4>', 'test-class')
    expected = '<h4 class="test-class"></h4>'
    assert actual == expected
