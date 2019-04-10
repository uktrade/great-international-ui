from django.conf import settings
from directory_constants.constants import urls


def footer_contact_us_link(request):
    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = urls.build_great_url('international/contact/')
    else:
        footer_contact_us_link = urls.CONTACT_US

    return {
        'footer_contact_us_link': footer_contact_us_link
    }
