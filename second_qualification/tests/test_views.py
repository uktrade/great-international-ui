import pytest
from unittest.mock import patch

from django.urls import reverse

from second_qualification import forms, views


@pytest.fixture
def form_data():
    return {
        'emt_id': 42,
        'phone_number': '0000000000',
        'arrange_callback': forms.ARRANGE_CALLBACK_CHOICES[0][0],
    }


@patch.object(views.SecondQualificationFormView.form_class, 'save')
def test_second_qualification_form_success(mock_save, form_data, rf):
    url = reverse('second-qualification')

    request = rf.post(url, data=form_data)
    request.LANGUAGE_CODE = 'en-gb'
    request.utm = {}
    response = views.SecondQualificationFormView.as_view()(request)

    assert response.status_code == 302
    assert response.url == reverse('second-qualification-success')

    assert mock_save.call_count == 1


def test_second_qualification_success(rf):
    url = reverse('second-qualification')

    request = rf.get(url)
    request.LANGUAGE_CODE = 'en-gb'
    request.utm = {}
    response = views.SecondQualificationSuccessView.as_view()(request)
    context_data = response.context_data

    assert response.status_code == 200
    assert context_data.get('ga360', {}).get('page_id') == 'SecondQualificationFormSuccess'


@patch.object(views.SecondQualificationFormView.form_class, 'save')
def test_second_qualification_invalid(mock_save, rf):
    url = reverse('second-qualification')
    utm_data = {
        'utm_source': 'test_source',
        'utm_medium': 'test_medium',
        'utm_campaign': 'test_campaign',
        'utm_term': 'test_term',
        'utm_content': 'test_content'
    }

    request = rf.post(url, data={})
    request.LANGUAGE_CODE = 'en-gb'
    request.utm = utm_data
    response = views.SecondQualificationFormView.as_view()(request)

    assert response.status_code == 200

    assert mock_save.call_count == 0
    assert response.context_data['form'].utm_data == utm_data


def test_invest_contact_form_view(client):
    response = client.get(reverse('second-qualification'))
    assert 'fair-processing-notice-invest-in-great-britain' in response.context_data['privacy_url']
    assert response.status_code == 200
