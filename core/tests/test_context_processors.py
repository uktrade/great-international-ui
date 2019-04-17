from django.utils import translation

from directory_constants import urls

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


def test_directory_components_html_lang_attribute(settings):

    with translation.override('fr'):
        actual = context_processors.directory_components_html_lang_attribute(None)  # noqa

        assert actual[
            'directory_components_html_lang_attribute'
        ] == translation.get_language()

    with translation.override('de'):
        actual = context_processors.directory_components_html_lang_attribute(None)  # noqa

        assert actual[
            'directory_components_html_lang_attribute'
        ] == translation.get_language()
