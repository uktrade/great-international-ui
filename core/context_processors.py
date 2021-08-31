from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from directory_constants import urls
from core import header_config


def footer_contact_us_link(request):
    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = urls.international.HOME / 'contact'
    else:
        footer_contact_us_link = urls.international.CONTACT

    return {
        'footer_contact_us_link': footer_contact_us_link
    }


def directory_components_html_lang_attribute(request):
    return {
        'directory_components_html_lang_attribute': translation.get_language()
    }


def services_home_links(request):
    return {
        'international_home_link': {
            'url': reverse_lazy('index'),
            'label': _('great.gov.uk international')
        },
        'trade_home_link': {
            'url': reverse_lazy('find-a-supplier:trade-home'),
            'label': _('Find a supplier')
        },
        'invest_home_link': {
            'url': reverse_lazy('invest-home'),
            'label': _('Invest')
        },
        'investment_atlas_home_link': {
            'url': reverse_lazy('atlas-home'),
            'label': _('Invest in the UK')
        },
    }


def header_navigation(request):
    nav_tree = header_config.nav_tree.ATLAS_HEADER_TREE \
        if settings.FEATURE_FLAGS['NEW_IA_ON'] \
        else header_config.nav_tree.OLD_HEADER_TREE

    return {
        'navigation_tree': nav_tree
    }
