import pytest

from django.urls import reverse

from directory_constants.constants.choices import COUNTRY_CHOICES

from core import helpers


@pytest.mark.parametrize('path,expected_prefix', (
    ('/', 'en-gb'),
    ('/ar/', 'ar'),
    ('/es/industries/', 'es'),
    ('/zh-hans/industries/', 'zh-hans'),
    ('/de/industries/aerospace/', 'de'),
    ('/fr/industries/automotive/', 'fr'),
))
def test_get_language_from_prefix(client, path, expected_prefix):
    prefix = helpers.get_language_from_prefix(path)
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


@pytest.mark.parametrize('country_code,country_name', COUNTRY_CHOICES)
def test_get_country_from_querystring(country_code, country_name, rf):
    url = reverse('index')
    request = rf.get(url, {'country': country_code})

    actual = helpers.get_country_from_querystring(request)

    assert actual == country_code


def test_get_country_from_querystring_invalid_code(rf):
    url = reverse('index')
    request = rf.get(url, {'country': 'foo'})

    actual = helpers.get_country_from_querystring(request)

    assert not actual
