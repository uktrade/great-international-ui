import pytest

from django.forms.fields import Field
from unittest import mock

from directory_validators.url import not_contains_url_or_email
from directory_constants import choices

from find_a_supplier import forms, views
from core.tests.helpers import create_response


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
    form = forms.SubscribeForm()

    assert form.is_valid() is False
    assert form.fields['full_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['sector'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['terms'].required is True


@pytest.fixture
def test_subscribe_form_accepts_valid_data(captcha_stub):
    form = forms.SubscribeForm(data={
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'DE',
        'terms': True,
        'g-recaptcha-response': captcha_stub
    })

    assert form.is_valid()


@mock.patch('directory_api_client.client.api_client.buyer.send_form')
def test_subscribe_form_view_valid_data(mock_send_form, captcha_stub):
    form = forms.SubscribeForm(data={
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'DE',
        'terms': True,
        'g-recaptcha-response': captcha_stub
    })
    mock_send_form.return_value = create_response()

    assert form.is_valid()

    assert views.SubscribeFormView().form_valid(form)


def test_contact_company_form_required_fields():
    form = forms.ContactCompanyForm()

    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['sector'].required is True
    assert form.fields['subject'].required is True
    assert form.fields['body'].required is True


def test_contact_company__form_length_of_fields():
    form = forms.ContactCompanyForm()

    assert form.fields['given_name'].max_length == 255
    assert form.fields['family_name'].max_length == 255
    assert form.fields['company_name'].max_length == 255
    assert form.fields['country'].max_length == 255
    assert form.fields['subject'].max_length == 200
    assert form.fields['body'].max_length == 1000


def test_contact_company_form_capcha_valid(captcha_stub):
    form = forms.ContactCompanyForm({'g-recaptcha-response': captcha_stub})

    form.is_valid()

    assert 'captcha' not in form.errors


def test_contact_company_form_captcha_invalid():
    form = forms.ContactCompanyForm({})

    assert form.is_valid() is False
    assert 'captcha' in form.errors


@mock.patch(
    'directory_forms_api_client.client.forms_api_client.submit_generic'
)
def test_contact_supplier_body_text(
    mock_submit_generic, valid_contact_company_data, captcha_stub
):
    form = forms.ContactCompanyForm(data=valid_contact_company_data)

    assert form.is_valid()

    form.save(
        template_id='foo',
        email_address='reply_to@example.com',
        form_url='/trade/some/path/',
    )

    assert form.serialized_data == {
        'email_address': valid_contact_company_data['email_address'],
        'body': valid_contact_company_data['body'],
        'company_name': valid_contact_company_data['company_name'],
        'given_name': valid_contact_company_data['given_name'],
        'family_name': valid_contact_company_data['family_name'],
        'terms': True,
        'sector': valid_contact_company_data['sector'],
        'sector_label': 'Aerospace',
        'country': valid_contact_company_data['country'],
        'subject': valid_contact_company_data['subject'],
        'captcha': captcha_stub,
    }


def test_contact_company_validators():
    form = forms.ContactCompanyForm({})
    validator = not_contains_url_or_email

    assert validator in form.fields['given_name'].validators
    assert validator in form.fields['family_name'].validators
    assert validator in form.fields['company_name'].validators
    assert validator in form.fields['country'].validators
    assert validator in form.fields['subject'].validators
    assert validator in form.fields['body'].validators


def test_search_form():
    form = forms.CompanySearchForm(data={
        'q': '123',
        'industries': ['AEROSPACE']
    })

    assert form.is_valid() is True
    assert form.cleaned_data['q'] == '123'
    assert form.cleaned_data['industries'] == ['AEROSPACE']


def test_search_required_fields():
    form = forms.CompanySearchForm()

    assert form.fields['industries'].required is False
    assert form.fields['q'].required is False


def test_search_required_empty_sector_term():
    form = forms.CompanySearchForm(data={'q': '', 'industries': ''})

    assert form.is_valid() is False

    assert form.errors == {
        '__all__': [forms.CompanySearchForm.MESSAGE_MISSING_SECTOR_TERM]
    }


def test_contact_required_fields():
    form = forms.BuyFromTheUKForm(data={})

    assert form.is_valid() is False
    assert form.errors == {
        'body': ['This field is required.'],
        'captcha': ['This field is required.'],
        'country': ['This field is required.'],
        'email_address': ['This field is required.'],
        'given_name': ['This field is required.'],
        'family_name': ['This field is required.'],
        'organisation_name': ['This field is required.'],
        'phone_number': ['This field is required.'],
        'sector': ['This field is required.'],
    }


def test_contact_invalid_country(valid_contact_data):
    data = valid_contact_data
    data['country'] = 'fake country'
    form = forms.BuyFromTheUKForm(data=data)

    assert form.is_valid() is False
    assert form.errors == {
        'country': ['Select a valid choice. fake country is not one of the available choices.'],
    }


@mock.patch('directory_forms_api_client.client.forms_api_client.submit_generic')
def test_contact_body_text(mock_submit_generic, valid_contact_data):
    mock_submit_generic.return_value = None
    form = forms.BuyFromTheUKForm(data=valid_contact_data)

    assert form.is_valid()

    form.save(
        template_id='foo',
        email_address='reply_to@example.com',
        form_url='/trade/some/path/',
    )

    assert form.serialized_data == {
        'body': valid_contact_data['body'],
        'country': valid_contact_data['country'],
        'country_name': choices.COUNTRIES_AND_TERRITORIES[0][1],
        'email_address': valid_contact_data['email_address'],
        'organisation_name': valid_contact_data['organisation_name'],
        'organisation_size': choices.EMPLOYEES[0][1],
        'sector': choices.sectors.AEROSPACE,
        'source': '',
        'source_other': '',
        'given_name': valid_contact_data['given_name'],
        'family_name': valid_contact_data['family_name'],
        'email_contact_consent': valid_contact_data['email_contact_consent'],
        'telephone_contact_consent': valid_contact_data['telephone_contact_consent'],
        'phone_number': valid_contact_data['phone_number']
    }
