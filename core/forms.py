from directory_components import forms, fields, helpers
from django.forms import Select
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.widgets import HiddenInput
from core.fields import IntegerField

from directory_constants.choices import COUNTRY_CHOICES

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


class TariffsCountryForm(forms.Form):
    tariffs_country = fields.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-tariffs-country-select'}),
        choices=COUNTRIES
    )


class OpportunitySearchForm(forms.Form):

    page = IntegerField(
        required=False,
        widget=HiddenInput,
        initial=1,
    )

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial
