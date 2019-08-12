import os
from unittest import mock

from directory_api_client.client import api_client
import pytest

from django.conf import settings
from django.utils import translation

from core import context_processors
from core.tests.helpers import create_response


@pytest.fixture()
def captcha_stub():
    # https://github.com/praekelt/django-recaptcha#id5
    os.environ['RECAPTCHA_TESTING'] = 'True'
    yield 'PASSED'
    os.environ['RECAPTCHA_TESTING'] = 'False'


@pytest.fixture
def default_context():
    return context_processors.services_home_links(None)


@pytest.fixture
def breadcrumbs():
    return {
        'landingpage': {
            'slug': 'home',
        },
        'industrylandingpage': {
            'slug': 'industries',
        },
        'industrycontactpage': {
            'slug': 'contact-us'
        },
    }


@pytest.fixture(autouse=True)
def set_language_to_default():
    translation.activate(settings.LANGUAGE_CODE)


@pytest.fixture(autouse=True)
def feature_flags(settings):
    # solves this issue: https://github.com/pytest-dev/pytest-django/issues/601
    settings.FEATURE_FLAGS = {**settings.FEATURE_FLAGS}
    yield settings.FEATURE_FLAGS


@pytest.fixture
def retrieve_profile_data():
    return {
        'website': 'http://example.com',
        'description': 'Ecommerce website',
        'summary': 'this is a short summary',
        'number': '01234567',
        'sectors': ['SECURITY'],
        'logo': 'nice.jpg',
        'name': 'Great company',
        'slug': 'great-company',
        'keywords': 'word1, word2',
        'employees': '501-1000',
        'date_of_creation': '2015-03-02',
        'verified_with_code': True,
        'twitter_url': 'http://www.twitter.com',
        'facebook_url': 'http://www.facebook.com',
        'linkedin_url': 'http://www.linkedin.com',
        'supplier_case_studies': [],
        'modified': '2016-11-23T11:21:10.977518Z',
        'email_full_name': 'Jeremy',
        'email_address': 'test@example.com',
        'postal_full_name': 'Jeremy',
        'address_line_1': '123 Fake Street',
        'address_line_2': 'Fakeville',
        'locality': 'London',
        'postal_code': 'E14 6XK',
        'po_box': 'abc',
        'country': 'GB',
        'mobile_number': '07506043448',
        'company_type': 'COMPANIES_HOUSE',
        'is_published_investment_support_directory': True,
        'is_published_find_a_supplier': True,
    }


@pytest.fixture
def supplier_case_study_data(retrieve_profile_data):
    return {
        'description': 'Damn great',
        'sector': 'SOFTWARE_AND_COMPUTER_SERVICES',
        'image_three': 'https://image_three.jpg',
        'website': 'http://www.google.com',
        'video_one': 'https://video_one.wav',
        'title': 'Two',
        'slug': 'two',
        'company': retrieve_profile_data,
        'image_one': 'https://image_one.jpg',
        'testimonial': 'I found it most pleasing.',
        'keywords': 'great',
        'pk': 2,
        'year': '2000',
        'image_two': 'https://image_two.jpg'
    }


@pytest.fixture(autouse=True)
def retrieve_supplier_case_study(supplier_case_study_data):
    stub = mock.patch.object(
        api_client.company, 'retrieve_public_case_study',
        return_value=create_response(supplier_case_study_data),
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture
def search_results(retrieve_profile_data):
    return {
        'hits': {
            'total': 1,
            'hits': [
                {
                    '_source': retrieve_profile_data

                }
            ]
        }
    }


@pytest.fixture
def search_results_description_highlight(search_results):
    search_results['hits']['hits'][0]['highlight'] = {
        'description': [
            '<em>wolf</em> in sheep clothing description',
            'to the max <em>wolf</em>.'
        ]
    }
    return search_results


@pytest.fixture
def search_results_summary_highlight(search_results):
    search_results['hits']['hits'][0]['highlight'] = {
        'summary': ['<em>wolf</em> in sheep clothing summary.']
    }
    return search_results
