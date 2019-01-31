from django.conf import settings
from core.helpers import get_untranslated_url
from directory_constants.constants import urls


def untranslated_url(request):
    untranslated_url = get_untranslated_url(request.path)
    return {
        'untranslated_url': untranslated_url
    }


def footer_contact_us_link(request):
    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = urls.build_great_url('international/contact/')
    else:
        footer_contact_us_link = urls.CONTACT_US

    return {
        'footer_contact_us_link': footer_contact_us_link
    }
