from core.templatetags import cms_tags


def test_prefix_path():
    actual = cms_tags.prefix_path('/article-list/article-slug/')
    expected = '/international/article-list/article-slug/'
    assert actual == expected
