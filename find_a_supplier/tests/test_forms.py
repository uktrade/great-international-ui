import pytest

from django.forms.fields import Field

from find_a_supplier import forms


REQUIRED_MESSAGE = Field.default_error_messages['required']


def test_serialize_anonymous_subscriber_forms():
    data = {
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Example corp',
        'country': 'UK',
    }
    expected = {
        'name': 'Jim Example',
        'email': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Example corp',
        'country': 'UK',
    }
    actual = forms.serialize_anonymous_subscriber_forms(data)

    assert actual == expected


def test_subscribe_form_required():
    form = forms.AnonymousSubscribeForm()

    assert form.is_valid() is False
    assert form.fields['full_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['sector'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['terms'].required is True


@pytest.fixture
def test_subscribe_form_accepts_valid_data(captcha_stub):
    form = forms.AnonymousSubscribeForm(data={
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'DE',
        'terms': True,
        'g-recaptcha-response': captcha_stub
    })

    assert form.is_valid()
