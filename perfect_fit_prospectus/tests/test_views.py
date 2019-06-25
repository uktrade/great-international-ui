import pytest
from unittest import mock

from botocore.exceptions import ClientError
from unittest.mock import patch, MagicMock

from django.urls import reverse
from requests import HTTPError

OPTIONS_DATA = {
    "country": {
        "choices": [
            {
                "value": "AF",
                "display_name": "Afghanistan"
            },
        ]
    },
    "market": {
        "choices": [
            {
                "value": "africa",
                "display_name": "africa"
            },
            {
                "value": "canada",
                "display_name": "canada"
            }
        ]
    },
    "sector": {
        "choices": [
            {
                "value": "tech",
                "display_name": "Technology"
            },
            {
                "value": "automotive",
                "display_name": "Automotive"
            },
        ]
    }
}


@patch('pir_client.client.pir_api_client.get_options')
def test_perfect_fit_main_view_get(mock_get_options, client):
    mock_get_options.return_value = OPTIONS_DATA
    url = reverse('perfect_fit_prospectus:main')
    response = client.get(url)
    assert response.status_code == 200


@patch('pir_client.client.pir_api_client.get_options')
def test_perfect_fit_main_view_get_error(mock_get_options, client):
    mock_get_options.side_effect = HTTPError
    with pytest.raises(HTTPError):
        url = reverse('perfect_fit_prospectus:main')
        response = client.get(url)
        assert response.status_code == 500


@patch('pir_client.client.pir_api_client.create_report')
@patch('pir_client.client.pir_api_client.get_options')
def test_perfect_fit_main_view_post_client_error(
    mock_get_options, mock_create_report, client, captcha_stub
):
    mock_get_options.return_value = OPTIONS_DATA
    mock_create_report.side_effect = HTTPError

    valid_data = {
        'name': 'Ted',
        'company': 'Corp',
        'email': 'ted@example.com',
        'country': 'US',
        'sector': 'tech',
        'g-recaptcha-response': captcha_stub,
        'gdpr_optin': 'on'
    }
    url = reverse('perfect_fit_prospectus:main')
    with pytest.raises(HTTPError):
        client.post(url, data=valid_data)


@patch('pir_client.client.pir_api_client.create_report')
@patch('pir_client.client.pir_api_client.get_options')
def test_perfect_fit_main_view_post_valid_data(
    mock_get_options, mock_create_report, captcha_stub, client
):
    mock_get_options.return_value = OPTIONS_DATA

    valid_data = {
        'name': 'Ted',
        'company': 'Corp',
        'email': 'ted@example.com',
        'country': 'US',
        'sector': 'tech',
        'g-recaptcha-response': captcha_stub,
        'gdpr_optin': 'on'
    }

    url = reverse('perfect_fit_prospectus:main')
    response = client.post(url, data=valid_data)
    assert response.status_code == 302

    success_response = client.post(
        url, data=valid_data, follow=True)
    assert success_response.status_code == 200

    messages = [
        message.message for message in
        list(success_response.context['messages'])]
    assert 'ted@example.com' in messages[0]

    assert mock_create_report.called is True
    assert mock_create_report.call_args == mock.call(
        {
            'name': 'Ted', 'company': 'Corp', 'email': 'ted@example.com',
            'phone_number': '', 'country': 'US', 'gdpr_optin': True,
            'captcha': 'PASSED', 'sector': 'tech'
        }
    )


@patch('perfect_fit_prospectus.views.boto3')
def test_perfect_fit_report_proxy_view_success(mock_boto3, client):
    mock_boto3.client().generate_presigned_url.return_value = (
        'http://www.example.com/test.pdf'
    )

    url = reverse(
        'perfect_fit_prospectus:report',
        kwargs={'filename': 'test.pdf'}
    )
    response = client.get(url)
    assert response['location'] == 'http://www.example.com/test.pdf'


@patch('perfect_fit_prospectus.views.boto3')
def test_perfect_fit_report_proxy_view_key_not_found(mock_boto3, client):
    mock_boto3.client().head_object.side_effect = ClientError(
        MagicMock(), MagicMock()
    )
    url = reverse(
        'perfect_fit_prospectus:report',
        kwargs={'filename': 'test.pdf'}
    )
    response = client.get(url)
    assert response.status_code == 404
