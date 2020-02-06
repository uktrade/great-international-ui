import pytest
from directory_constants import choices

from euexit import forms


@pytest.fixture
def international_contact_form_data(captcha_stub):
    return {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRIES_AND_TERRITORIES[1][0],
        'city': 'London',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


@pytest.mark.parametrize(
    'country_name,form_is_valid,expected_error',
    (
        (choices.COUNTRIES_AND_TERRITORIES[2][0], True, None),
        ('HK', True, None),
        ('AE-AJ', False, {'country': ['Select a valid choice. AE-AJ is not one of the available choices.']}),
    )
)
def test_international_contact_form_serialize(captcha_stub, country_name, form_is_valid, expected_error):
    form = forms.TransitionContactForm(
        ingress_url='http://www.ingress.com',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': country_name,
            'city': 'London',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
            'email_contact_consent': True,
            'telephone_contact_consent': False
        }
    )

    assert form.is_valid() is form_is_valid
    if form_is_valid:
        assert form.serialized_data == {
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': country_name,
            'city': 'London',
            'comment': 'hello',
            'ingress_url': 'http://www.ingress.com',
            'email_contact_consent': True,
            'telephone_contact_consent': False
        }
    if expected_error:
        assert form.errors == expected_error
