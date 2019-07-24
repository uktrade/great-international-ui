from django.urls import reverse
from unittest.mock import patch

from core import helpers


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_google_campaign_middleware(mock_lookup_by_path, client):
    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'InternationalHomePage'
    }

    mock_lookup_by_path.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )
    url = reverse('index')
    client.get(
        url,
        {
            'utm_source': 'test_source',
            'utm_medium': 'test_medium',
            'utm_campaign': 'test_campaign',
            'utm_term': 'test_term',
            'utm_content': 'test_content'
        })

    correct_utm = {
        'utm_source': 'test_source',
        'utm_medium': 'test_medium',
        'utm_campaign': 'test_campaign',
        'utm_term': 'test_term',
        'utm_content': 'test_content'
    }

    assert 'utm' in client.session
    assert client.session['utm'] == correct_utm
