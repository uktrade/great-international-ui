import pytest
from django.urls import reverse
from unittest.mock import patch

from contact import forms, views


@pytest.fixture
def contact_form_data(captcha_stub):
    return {
        'name': 'Scrooge McDuck',
        'email': 'sm@example.com',
        'job_title': 'President',
        'phone_number': '0000000000',
        'company_name': 'Acme',
        'country': 'United States',
        'staff_number': forms.STAFF_CHOICES[0][0],
        'description': 'foobar',
        'g-recaptcha-response': captcha_stub,
    }


@patch.object(views.ContactFormView.form_class, 'save')
def test_contact_form_success(mock_save, contact_form_data, rf):
    url = reverse('invest-contact')

    request = rf.post(url, data=contact_form_data)
    request.LANGUAGE_CODE = 'en-gb'
    request.utm = {}
    response = views.ContactFormView.as_view()(request)

    assert response.status_code == 302
    assert response.url == reverse('invest-contact-success')

    assert mock_save.call_count == 1


@patch.object(views.ContactFormView.form_class, 'save')
def test_contact_invalid(mock_save, rf):
    url = reverse('invest-contact')
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
    response = views.ContactFormView.as_view()(request)

    assert response.status_code == 200

    assert mock_save.call_count == 0
    assert response.context_data['form'].utm_data == utm_data
