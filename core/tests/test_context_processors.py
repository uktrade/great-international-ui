import pytest
from unittest.mock import patch
from directory_constants.constants import urls
from directory_constants.constants.choices import COUNTRY_CHOICES

from core import context_processors


def test_footer_contact_link_processor_flag_on_settings(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': True,
    }

    actual = context_processors.footer_contact_us_link(None)

    expected = urls.build_great_url('international/contact/')
    assert actual['footer_contact_us_link'] == expected


def test_footer_contact_link_processor_flag(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': False,
    }

    actual = context_processors.footer_contact_us_link(None)

    assert actual['footer_contact_us_link'] == urls.CONTACT_US


@pytest.mark.parametrize('country_code,country_name', COUNTRY_CHOICES)
@patch('core.helpers.get_user_country')
def test_user_country_processor(
    mock_get_user_country, country_code, country_name
):
    mock_get_user_country.return_value = country_code

    actual = context_processors.user_country(None)

    assert actual['country']['code'] == country_code.lower()
    assert actual['country']['name'] == country_name
    assert actual['hide_country_selector']


@patch('core.helpers.get_user_country')
def test_user_country_processor_no_code(mock_get_user_country):
    mock_get_user_country.return_value = ''

    actual = context_processors.user_country(None)

    assert actual['country']['code'] == ''
    assert actual['country']['name'] == ''
    assert not actual['hide_country_selector']
