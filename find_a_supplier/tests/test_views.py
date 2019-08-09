import pytest
import http
from unittest.mock import patch

from django.core.urlresolvers import reverse

from find_a_supplier.forms import SearchForm
from core.tests.helpers import create_response, stub_page


@pytest.fixture
def fas_home_page():
    yield from stub_page({
        'page_type': 'InternationalTradeHomePage',
    })


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_fas_homepage_search_form(mock_cms_response, fas_home_page, client):
    mock_cms_response.return_value = create_response(
        status_code=200,
        json_payload=fas_home_page.return_value.json()
    )

    url = reverse('trade-home')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['search_form'] == SearchForm


def test_anonymous_subscribe(client):
    response = client.get(reverse('trade-subscribe'))

    assert response.status_code == http.client.OK
