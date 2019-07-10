from captcha.fields import ReCaptchaField
from directory_components import forms, fields, helpers
from django.forms import Textarea, TextInput, Select, NumberInput
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from directory_validators.common import not_contains_url_or_email

from directory_constants import choices

COUNTRIES = BLANK_CHOICE_DASH + choices.COUNTRY_CHOICES


class EbookDetailsForm(forms.Form):

    def __init__(self, industry_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].choices = industry_choices

    name = fields.CharField(
        label=_('Name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        )
    )
    email_address = fields.EmailField(
        label=_('Email'),
        widget=TextInput(
            attrs={'dir': 'auto'}
        )
    )
    company = fields.CharField(
        label=_('Company'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        )
    )
    number_of_staff = fields.ChoiceField(
        label=_('Current number of staff'),
        choices=choices.EMPLOYEES,
        required=False,
    )
    sector = fields.ChoiceField(
        label=_('Sector'),
        choices=[],  # set in __init__
    )
    country = fields.ChoiceField(
        label=_('Country'),
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )

    expand = fields.BooleanField(
        label=_('Setting up a business in the UK'),
        required=False,
    )
    invest_capital = fields.BooleanField(
        label=_('Investing capital in the UK'),
        required=False,
    )
    buy_goods = fields.BooleanField(
        label=_('Buying goods from the UK'),
        required=False,
    )

    further_information = fields.BooleanField(
        label=_('I would like to receive further information')
    )
    terms_and_conditions = fields.BooleanField(
        label=_('I confirm the information provided is true and I accept DIT\'s terms and conditions')  # noqa
    )

    captcha = ReCaptchaField(label='', label_suffix='')


class CountryForm(forms.Form):
    country = fields.ChoiceField(
        label=_('Country'),
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )


def get_country_form_initial_data(request):
    return {
        'country': helpers.get_user_country(request).upper() or None
    }


class TariffsCountryForm(forms.Form):
    tariffs_country = fields.ChoiceField(
        label=_('Country'),
        widget=Select(attrs={'id': 'js-tariffs-country-select'}),
        choices=COUNTRIES
    )
