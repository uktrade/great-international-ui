from unittest.mock import patch

from directory_api_client.client import api_client
import pytest

from core.tests.helpers import create_response


@pytest.fixture
def valid_contact_company_data(captcha_stub):
    return {
        'given_name': 'Jim',
        'family_name': 'Example',
        'company_name': 'Example Corp',
        'country': 'China',
        'email_address': 'jim@example.com',
        'email_full_name': 'Jeremy',
        'sector': 'AEROSPACE',
        'subject': 'greetings',
        'body': 'and salutations',
        'g-recaptcha-response': captcha_stub,
        'terms': True,
    }


@pytest.fixture(autouse=True)
def published_profile_retrieve(retrieve_profile_data):
    stub = patch.object(
        api_client.company, 'published_profile_retrieve',
        return_value=create_response(retrieve_profile_data),
    )
    stub.start()
    yield
    stub.stop()
