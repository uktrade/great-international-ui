import pytest

from django.urls import reverse

from core import helpers


@pytest.mark.parametrize('path,expect_code', (
    ('/', None),
    ('?lang=pt', 'pt'),
    ('/?lang=ar', 'ar'),
    ('/industries?lang=es', 'es'),
    ('/industries/?lang=zh-hans', 'zh-hans'),
    ('/industries/aerospace?lang=de', 'de'),
    ('/industries/automotive/?lang=fr', 'fr'),
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
