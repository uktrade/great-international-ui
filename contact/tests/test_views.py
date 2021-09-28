import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup

from django.urls import reverse
from django.conf import settings

from conf.tests.test_urls import reload_urlconf
from contact import forms, views


@pytest.fixture
def contact_form_data(captcha_stub):
    return {
        'given_name': 'Scrooge',
        'family_name': 'McDuck',
        'job_title': 'President',
        'email': 'sm@example.com',
        'phone_number': '0000000000',
        'company_name': 'Acme',
        'company_website': 'www.test.com',
        'company_hq_address': 'London',
        'country': forms.COUNTRY_CHOICES[0][0],
        'industry': forms.INDUSTRIES[0][0],
        'expanding_to_uk': forms.EXPANDING_TO_UK_CHOICES[1][0],
        'description': 'lorum ipsum',
        'arrange_callback': forms.ARRANGE_CALLBACK_CHOICES[1][0],
        'how_did_you_hear': forms.HOW_DID_YOU_HEAR_CHOICES[1][0],
        'email_contact_consent': False,
        'telephone_contact_consent': False,
        'g-recaptcha-response': captcha_stub
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


@pytest.mark.skip("Skipping this test as disabled translation")
@pytest.mark.parametrize('url', (
    'invest-contact',
    'invest-contact-success'
))
def test_contact_pages_localised_urls(url, client, settings):
    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    url = reverse(url) + '?lang=de'
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    other_languages = [code for code, _ in settings.LANGUAGES if code != 'de']

    for code in other_languages:
        link_tag = soup.select(f'link[hreflang="{code}"]')[0]
        assert link_tag
        assert 'http://testserver' in link_tag.attrs['href']


@pytest.mark.parametrize(
    'language_code',
    [code for code, _ in settings.LANGUAGES],
)
def test_contact_pages_localised_urls_all_languages(language_code, client, settings):
    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    url = reverse('invest-contact') + f'?lang={language_code}'
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    other_languages = [code for code, _ in settings.LANGUAGES if code != language_code]

    for code in other_languages:
        link_tag = soup.select(f'link[hreflang="{code}"]')[0]
        assert link_tag
        assert 'http://testserver' in link_tag.attrs['href']


def test_invest_contact_form_view(client):
    response = client.get(reverse('invest-contact'))
    assert 'fair-processing-notice-invest-in-great-britain' in response.context_data['privacy_url']
    assert response.status_code == 200
