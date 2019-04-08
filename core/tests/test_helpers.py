import pytest

from core import helpers


@pytest.mark.parametrize('path,expected_prefix', (
    ('/', 'en-gb'),
    ('/?lang=ar', 'ar'),
    ('/industries?lang=es', 'es'),
    ('/industries/?lang=zh-hans', 'zh-hans'),
    ('/industries/aerospace?lang=de', 'de'),
    ('/industries/automotive/?lang=fr', 'fr'),
))
def test_get_language_from_querystring(client, path, expected_prefix):
    prefix = helpers.get_language_from_querystring(path)
    assert prefix == expected_prefix


@pytest.mark.parametrize('prefixed_url,exp_url', (
    ('/de/', '/'),
    ('/ar/', '/'),
    ('/es/industries/', '/industries/'),
    ('/zh-hans/industries/', '/industries/'),
    ('/de/industries/aerospace/', '/industries/aerospace/'),
    ('/fr/industries/automotive/', '/industries/automotive/'),
))
def test_get_untranslated_url(prefixed_url, exp_url):
    url = helpers.get_untranslated_url(prefixed_url)
    assert url == exp_url


unslugify_slugs = [
    ('test-slug-one', 'Test slug one'),
    ('test-two', 'Test two'),
    ('slug', 'Slug'),
]


@pytest.mark.parametrize('slug,exp', unslugify_slugs)
def test_unslugify(slug, exp):
    assert helpers.unslugify(slug) == exp
