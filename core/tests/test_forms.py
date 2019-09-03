from unittest.mock import call, patch

import pytest

from core.forms import CapitalInvestContactForm


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
