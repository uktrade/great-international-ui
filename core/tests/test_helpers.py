import pytest

from django.urls import reverse

from core import helpers


@pytest.mark.parametrize('path,expect_code', (
    ('/', None),
    ('?language=pt', 'pt'),
    ('/?language=ar', 'ar'),
    ('/industries?language=es', 'es'),
    ('/industries/?language=zh-hans', 'zh-hans'),
    ('/industries/aerospace?language=de', 'de'),
    ('/industries/automotive/?language=fr', 'fr'),
))
def test_get_language_from_querystring(path, expect_code, rf):
    url = reverse('index')
    request = rf.get(url + path)
    language_code = helpers.get_language_from_querystring(request)
    assert language_code == expect_code


unslugify_slugs = [
    ('test-slug-one', 'Test slug one'),
    ('test-two', 'Test two'),
    ('slug', 'Slug'),
]


@pytest.mark.parametrize('slug,exp', unslugify_slugs)
def test_unslugify(slug, exp):
    assert helpers.unslugify(slug) == exp
