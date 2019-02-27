from directory_components import forms, fields
from django.forms import Select
from django.db.models.fields import BLANK_CHOICE_DASH

from directory_constants.constants.choices import COUNTRY_CHOICES

from core import helpers

COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES


class CountryForm(forms.Form):
    country = fields.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )


def get_country_form_initial_data(request):
    return {
        'country': helpers.get_user_country(request).upper() or None
    }
