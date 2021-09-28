import pytest
from unittest.mock import patch
from django.urls import reverse

from conf.tests.test_urls import reload_urlconf
from core.tests.helpers import create_response
from . import helpers


@pytest.mark.parametrize('source,destination', [
    (
        'high-potential-opportunities/rail-infrastructure',
        '/international/content/invest/high-potential-opportunities/rail-infrastructure/'
    ),
    (
        'high-potential-opportunities/food-production',
        '/international/content/invest/high-potential-opportunities/food-production/'
    ),
    (
        'high-potential-opportunities/lightweight-structures',
        '/international/content/invest/high-potential-opportunities/lightweight-structures/'
    ),
    (
        'high-potential-opportunities/rail-infrastructure/contact',
        '/international/content/invest/high-potential-opportunities/contact/'
    ),
    (
        'high-potential-opportunities/food-production/contact',
        '/international/content/invest/high-potential-opportunities/contact/'
    ),
    (
        'high-potential-opportunities/lightweight-structures/contact',
        '/international/content/invest/high-potential-opportunities/contact/'
    ),
    (
        'foo/bar',
        '/international/invest/'
    )
])
def test_invest_english_only_redirects(source, destination, client):
    url = reverse('invest-incoming', kwargs={'path': source})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == destination


@pytest.mark.parametrize('source,destination', helpers.generate_translated_redirects_tests_params())
def test_invest_translated_redirects(source, destination, client):
    url = reverse('invest-incoming', kwargs={'path': source})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == destination


def test_invest_redirects_persist_querystrings(client):
    url = reverse('invest-incoming', kwargs={'path': '/es/industries/'})
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/content/industries/?foo=bar&lang=es'


def test_invest_redirect_homepage(client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    url = reverse('invest-incoming', kwargs={'path': '/es/'})
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/invest/?foo=bar&lang=es'


def test_invest_redirect_homepage_english(client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    url = reverse('invest-incoming-homepage')
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/invest/?foo=bar'


@pytest.mark.skip("No longer relevant - users are redirected before they get here")
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_uk_region_page_cms_view(mock_get_page, client):
    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'languages': [['en-gb', 'English']],
                'slug': 'region-slug',
            },
            'page_type': 'InvestRegionPage',
        }
    )

    url = reverse('cms-page-from-path', kwargs={'path': 'invest/uk-regions/region-slug'})
    response = client.get(url)

    assert response.status_code == 200
