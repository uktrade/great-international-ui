import pytest
from django.urls import reverse

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
            '/international/investment/'
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


def test_invest_redirect_homepage(client):
    url = reverse('invest-incoming', kwargs={'path': '/es/'})
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/invest/?foo=bar&lang=es'
