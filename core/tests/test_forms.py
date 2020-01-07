import pytest
from unittest.mock import patch

from django.urls import reverse

from core import constants
from core.forms import (
    CapitalInvestContactForm, BusinessEnvironmentGuideForm, InternationalRoutingForm, WhyBuyFromUKForm
)
from core.views import BusinessEnvironmentGuideFormView
from core.tests.helpers import create_response


@pytest.fixture
def capital_invest_contact_form_data(captcha_stub):
    return {
        'given_name': 'Thor',
        'family_name': 'Odinson',
        'email_address': 'most_powerful_avenger@avengers.com',
        'phone_number': '01234 567891',
        'country': 'FR',
        'city': 'Asgard',
        'company_name': 'Guardian of the Galaxy',
        'message': 'foobar',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


@pytest.fixture
def business_environment_form_data(captcha_stub):
    return {
        'given_name': 'Thor',
        'family_name': 'Odinson',
        'email_address': 'most_powerful_avenger@avengers.com',
        'phone_number': '01234567899',
        'country': 'FR',
        'company_name': 'Guardian of the Galaxy',
        'industry': 'ADVANCED_MANUFACTURING',
        'email_contact_consent': True,
        'telephone_contact_consent': True,
        'g-recaptcha-response': captcha_stub,
    }


def test_capital_invest_contact_form_required():
    form = CapitalInvestContactForm()

    assert form.is_valid() is False
    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['country'].required is True
    assert form.fields['city'].required is False
    assert form.fields['message'].required is True
    assert form.fields['captcha'].required is True
    assert form.fields['terms_agreed'].required is True


def test_capital_invest_contact_form_accept_valid_data(captcha_stub, capital_invest_contact_form_data):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data
    )
    assert form.is_valid()


def test_capital_invest_contact_form_capcha_valid(captcha_stub):
    form = CapitalInvestContactForm({'g-recaptcha-response': captcha_stub})

    form.is_valid()

    assert 'captcha' not in form.errors


def test_capital_invest_contact_form_captcha_invalid():
    form = CapitalInvestContactForm({})

    assert form.is_valid() is False
    assert 'captcha' in form.errors


def test_capital_invest_contact_form_invalid_data(captcha_stub):
    form = CapitalInvestContactForm(
        data={
            'given_name': 'Steve',
            'family_name': 'Rogers',
            'country': 'FR',
            'message': 'foobar',
            'g-recaptcha-response': captcha_stub,
            'terms_agreed': True
        }
    )
    assert form.errors == {'email_address': ['This field is required.']}
    assert form.is_valid() is False


def test_business_environment_form_required():
    form = BusinessEnvironmentGuideForm()

    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['phone_number'].required is False
    assert form.fields['country'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['industry'].required is True
    assert form.fields['email_contact_consent'].required is False
    assert form.fields['telephone_contact_consent'].required is False
    assert form.fields['captcha'].required is True


def test_business_environment_serialized_data(business_environment_form_data):
    form = BusinessEnvironmentGuideForm(data=business_environment_form_data)
    form.full_clean()

    data = form.serialized_data

    assert 'given_name' in data
    assert 'family_name' in data
    assert 'email_address' in data
    assert 'phone_number' in data
    assert 'country' in data
    assert 'company_name' in data
    assert 'industry' in data
    assert 'email_contact_consent' in data
    assert 'telephone_contact_consent' in data
    assert 'captcha' not in data


def test_business_environment_form_accepts_valid_data(business_environment_form_data):
    form = BusinessEnvironmentGuideForm(data=business_environment_form_data)
    assert form.is_valid()


@patch.object(BusinessEnvironmentGuideFormView.form_class, 'save')
def test_business_environment_form_submission(mock_save, business_environment_form_data, client):
    mock_save.return_value = create_response(status_code=200)

    response = client.post(reverse('business-environment-guide-form'), business_environment_form_data)

    assert mock_save.call_count == 2
    assert response.status_code == 302
    assert response.url == reverse('business-environment-guide-form-success')


@pytest.fixture
def why_buy_from_the_uk_form_data():
    return {
        'name': 'Test User',
        'email_address': 'me@here.com',
        'company_name': 'Company LTD',
        'job_title': 'Director',
        'phone_number': '07777777777',
        'country': 'FR',
        'industry': 'ADVANCED_MANUFACTURING',
        'procuring_products': 'yes',
        'contact_email': False,
        'contact_phone': True,
        'city': 'London',
    }


def test_why_buy_from_the_uk_form_required():
    form = WhyBuyFromUKForm()
    assert form.fields['name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['phone_number'].required is True
    assert form.fields['city'].required is False
    assert form.fields['industry'].required is False
    assert form.fields['country'].required is True
    assert form.fields['procuring_products'].required is True
    assert form.fields['additional_requirements'].required is False
    assert form.fields['contact_email'].required is False
    assert form.fields['contact_phone'].required is False
    assert form.fields['procuring_products'].nested_form.fields['provide_more_info'].required is False


def test_why_buy_from_the_uk_form_serialized_data(why_buy_from_the_uk_form_data):
    form = WhyBuyFromUKForm(data=why_buy_from_the_uk_form_data)
    form.full_clean()

    data = form.serialized_data

    assert 'name' in data
    assert 'email_address' in data
    assert 'company_name' in data
    assert 'job_title' in data
    assert 'phone_number' in data
    assert 'city' in data
    assert 'industry' in data
    assert 'procuring_products' in data
    assert 'provide_more_info' in data
    assert 'additional_requirements' in data
    assert 'contact_phone' in data
    assert 'contact_email' in data
    assert 'country' in data
    assert 'city' in data


def test_why_buy_from_the_uk_form_accepts_valid_data(why_buy_from_the_uk_form_data):
    form = WhyBuyFromUKForm(data=why_buy_from_the_uk_form_data)
    assert form.is_valid()


@pytest.mark.parametrize('value', (True, False,))
def test_routing_forms_capital_invest_feature_flag(value, feature_flags):
    feature_flags['CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'] = value
    choices = InternationalRoutingForm().fields['choice'].choices

    assert any(value == constants.CAPITAL_INVEST_CONTACT_URL for value, label in choices) is value


@pytest.mark.parametrize('value_one,value_two', [(True, True), (False, False), (True, False), (False, True)])
def test_routing_forms_feature_flag_for_int_routing_form(value_one, value_two, feature_flags):
    feature_flags['CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'] = value_one
    feature_flags['EXPORTING_TO_UK_ON'] = value_two

    choices = InternationalRoutingForm().fields['choice'].choices

    assert any(value == constants.CAPITAL_INVEST_CONTACT_URL for value, label in choices) is value_one
    assert any(value == constants.EXPORTING_TO_UK_CONTACT_URL for value, label in choices) is value_two
