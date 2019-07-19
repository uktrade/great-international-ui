from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from core.tests.helpers import create_response


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'meta': {'languages': [['en-gb', 'English']]},
            'page_type': 'InvestHighPotentialOpportunityDetailPage',
        }
    )

    url = '/international/content/invest/high-potential-opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'invest/high_potential_opportunity_detail.html'
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail_not_found(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(status_code=404)

    url = '/international/content/invest/high-potential-opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail_cms_retrieval_ok(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'title': '1234',
            'meta': {'languages': [['en-gb', 'English']]},
            'page_type': 'InvestHighPotentialOpportunityDetailPage',
        }
    )

    url = '/international/content/invest/high-potential-opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page'] == {
        'title': '1234', 'meta': {'languages': [['en-gb', 'English']]},
        'page_type': 'InvestHighPotentialOpportunityDetailPage',
    }


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail_cms_retrieval_not_ok(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(status_code=400)

    url = '/international/content/invest/high-potential-opportunities/rail/'

    with pytest.raises(HTTPError):
        client.get(url)
