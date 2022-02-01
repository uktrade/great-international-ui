from django.utils import translation
from django.urls import reverse_lazy

from directory_constants import urls

from core import context_processors, header_config


def test_footer_contact_link_processor_flag_on_settings(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': True,
    }

    actual = context_processors.footer_contact_us_link(None)

    expected = urls.international.HOME / 'contact'
    assert actual['footer_contact_us_link'] == expected


def test_footer_contact_link_processor_flag(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': False,
    }

    actual = context_processors.footer_contact_us_link(None)

    assert actual['footer_contact_us_link'] == urls.international.CONTACT


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


def test_services_home_links():
    actual = context_processors.services_home_links(None)
    assert actual == {
        'international_home_link': {
            'label': 'great.gov.uk international',
            'url': reverse_lazy('index')
        },
        'trade_home_link': {
            'url': reverse_lazy('find-a-supplier:trade-home'),
            'label': 'Find a supplier',
        },
        'investment_atlas_home_link': {
            'url': reverse_lazy('atlas-home'),
            'label': 'Invest in the UK'
        },
    }


def test_header_navigation_uses_atlas_config(settings):
    context = context_processors.header_navigation(None)
    assert context['navigation_tree'] == header_config.nav_tree.ATLAS_HEADER_TREE
