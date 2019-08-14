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


@pytest.fixture
def list_public_profiles_data(retrieve_profile_data):
    return {
        'results': [
            retrieve_profile_data,
        ],
        'count': 20,
    }


@pytest.fixture(autouse=True)
def list_public_profiles(list_public_profiles_data):
    stub = patch.object(
        api_client.company, 'list_public_profiles',
        return_value=create_response(list_public_profiles_data),
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def retrieve_profile(retrieve_profile_data):
    stub = patch.object(
        api_client.company, 'retrieve_private_profile',
        return_value=create_response(retrieve_profile_data),
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def retrieve_public_profile(retrieve_profile_data):
    stub = patch.object(
        api_client.company, 'retrieve_public_profile',
        return_value=create_response(retrieve_profile_data),
    )
    stub.start()
    yield
    stub.stop()
