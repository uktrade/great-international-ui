import os
from copy import deepcopy
import http

import requests
import pytest
from django.conf import settings
from django.utils import translation

from core import context_processors


@pytest.fixture()
def captcha_stub():
    # https://github.com/praekelt/django-recaptcha#id5
    os.environ['RECAPTCHA_TESTING'] = 'True'
    yield 'PASSED'
    os.environ['RECAPTCHA_TESTING'] = 'False'


@pytest.fixture
def default_context():
    return context_processors.site_home_link(None)


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
def api_response_200():
    response = requests.Response()
    response.status_code = http.client.OK
    response.json = lambda: deepcopy({})
    return response


@pytest.fixture
def api_response_search_200(api_response_200, search_results):
    api_response_200.json = lambda: search_results
    return api_response_200


@pytest.fixture
def api_response_400():
    response = requests.Response()
    response.status_code = 400
    return response


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
def api_response_search_description_highlight_200(
    api_response_200, search_results
):
    search_results['hits']['hits'][0]['highlight'] = {
        'description': [
            '<em>wolf</em> in sheep clothing description',
            'to the max <em>wolf</em>.'
        ]
    }
    api_response_200.json = lambda: search_results
    return api_response_200


@pytest.fixture
def api_response_search_summary_highlight_200(
    api_response_200, search_results
):
    search_results['hits']['hits'][0]['highlight'] = {
        'summary': ['<em>wolf</em> in sheep clothing summary.']
    }
    api_response_200.json = lambda: search_results
    return api_response_200
