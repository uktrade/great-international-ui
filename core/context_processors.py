from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from directory_constants import urls


def footer_contact_us_link(request):
    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = urls.build_great_url('international/contact/')
    else:
        footer_contact_us_link = urls.CONTACT_US

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
    }
