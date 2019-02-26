from django.conf import settings
from core import helpers
from directory_constants.constants import urls
from directory_constants.constants.choices import COUNTRY_CHOICES


def untranslated_url(request):
    untranslated_url = helpers.get_untranslated_url(request.path)
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


def user_country(request):
    country_code = helpers.get_user_country(request)
    hide_country_selector = bool(country_code)

    if country_code:
        country_name = [
            name for code, name in COUNTRY_CHOICES
            if code == country_code][0]
    else:
        country_name = ''

    return {
        # if there is a country already detected we can hide the selector
        'hide_country_selector': hide_country_selector,
        'country': {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }
    }
