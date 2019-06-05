from django.conf import settings
from django.utils import translation
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


def site_home_link(request):
    return {
        'site_home_link': {
            'url': reverse_lazy('index'),
            'label': 'Great.gov.uk International'
        }
    }
