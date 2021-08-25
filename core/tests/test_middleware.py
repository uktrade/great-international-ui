from django.test import modify_settings
from django.urls import reverse
from unittest.mock import patch
from unittest import skip

from core.tests.helpers import create_response


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

    mock_lookup_by_path.return_value = create_response(page)
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


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_microsoft_defender_safe_links_middleware_trims_pii(mock_get_page, client):
    calls = [
        (
            '/international/'
            + '?lang=zh-hans'
            + '<https://eur02.safelinks.protection.outlook.com/'
            + '?url=https://www.great.gov.uk/international/'
            + '?lang=zh-hans'
            + '&data=04|01|someone@example.com|52e1fcc870ff4ef072|8fa217ec|0|0|63748103|Unknown|TWFpbGZsb3d8eyJWI=|1000'
            + '&sdata=6pfgjx6NF3ZWP2TQQjdI1XuB5xx/HGm2sgaokntWjvk='
            + '&reserved=0',
            'lang=zh-hans<https://eur02.safelinks.protection.outlook.com/'
            + '?url=https://www.great.gov.uk/international/'
            + '?lang=zh-hans'
            + '&sdata=6pfgjx6NF3ZWP2TQQjdI1XuB5xx/HGm2sgaokntWjvk='
            + '&reserved=0',
        ),
        (
            '/international/invest/'
            + '<https://eur02.safelinks.protection.outlook.com/'
            + '?url=https://www.great.gov.uk/international/invest/'
            + '&data=04|01|someone@example.com|f852c1f4a2814bf1d0|8fa217ec|0|0|63749854|Unknown|TWFpbGZsb3d8eyJWI=|1000'
            + '&sdata=LISO/lFPrI++ZLbztFWfWhyQuTTdJDrgX5OYX+dR4Fo='
            + '&reserved=0>.',
            'url=https://www.great.gov.uk/international/invest/'
            + '&sdata=LISO/lFPrI++ZLbztFWfWhyQuTTdJDrgX5OYX+dR4Fo='
            + '&reserved=0>.',
        ),
        (
            '/international/trade/<https://eur02.safelinks.protection.outlook.com/'
            + '?url=https://www.great.gov.uk/international/trade/'
            + '&data=04|01|someone@example.com|717be13dae814422c8|30a43325|1|0|63749997|Unknown|TWFpbGZsb3d8eyJWI=|1000'
            + '&sdata=VwFyrskaWXwX9WY/GHHNh9Tqc6471gLjT+jfwkB2vag='
            + '&reserved=0',
            'url=https://www.great.gov.uk/international/trade/'
            + '&sdata=VwFyrskaWXwX9WY/GHHNh9Tqc6471gLjT+jfwkB2vag='
            + '&reserved=0',
        ),
        (
            '/international/content/opportunities/<https://eur02..safelinks.protection.outlook.com/'
            + '?url=https://www.great.gov.uk/international/content/opportunities/'
            + '&data=04|01|someone@example.com|cd323113628a419d7b|8fa217ec|0|0|63748721|Unknown|TWFpbGZsb3d8eyJWI=|1000'
            + '&sdata=RMR1sDN435f61sERPSfe8vtgTwluVrzePnSN8YehsnE='
            + '&reserved=0',
            'url=https://www.great.gov.uk/international/content/opportunities/'
            + '&sdata=RMR1sDN435f61sERPSfe8vtgTwluVrzePnSN8YehsnE='
            + '&reserved=0',
        ),
    ]

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InvestInternationalHomePage',
        }
    )

    for path, expected_query_string in calls:
        response = client.get(path)
        request = response.wsgi_request

        assert request.META['QUERY_STRING'] == expected_query_string


@skip("FIXME: this test only works when run on its own...")
@patch('django.urls.resolve')
@modify_settings(MIDDLEWARE={'prepend': ['core.middleware.DebugToolbarSkipGAMiddleware']})
def test_debug_toolbar_skip_ga_middleware(mock_resolve, client):
    mock_resolve.return_value.namespace = 'djdt'
    response = client.get("/__debug__/render_panel/")
    request = response.wsgi_request

    assert request.skip_ga360 is True
