from captcha.fields import ReCaptchaField
from directory_components import forms
from directory_validators.common import not_contains_url_or_email
from django.forms import Select, TextInput
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _

from directory_constants.choices import COUNTRY_CHOICES, EMPLOYEES

COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES


class TariffsCountryForm(forms.Form):
    tariffs_country = forms.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-tariffs-country-select'}),
        choices=COUNTRIES
    )


class OpportunitySearchForm(forms.Form):

    sector = forms.ChoiceField(
        label=_('sector'),
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    scale = forms.ChoiceField(
        label=_('scale'),
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-scale'},
            use_nice_ids=True,
        ),
        required=False
    )
    region = forms.ChoiceField(
        label=_('region'),
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-region'},
            use_nice_ids=True,
        ),
        required=False
    )
    sub_sector = forms.ChoiceField(
        label=_('sub_sector'),
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sub_sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    sort_by = forms.ChoiceField(
        label=_('sort_by'),
        widget=Select(
            attrs={
                'onchange': 'this.form.submit()'
            }
        ),
        required=False,
    )

    def __init__(
            self, sectors, scales, regions,
            sort_by_options, sub_sectors, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fields['sector'].choices = sectors
        self.fields['scale'].choices = scales
        self.fields['region'].choices = regions
        self.fields['sort_by'].choices = sort_by_options
        self.fields['sub_sector'].choices = sub_sectors


class EbookDetailsForm(forms.Form):

    def __init__(self, industry_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].choices = industry_choices

    name = forms.CharField(
        label=_('Name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        )
    )
    email_address = forms.EmailField(
        label=_('Email'),
        widget=TextInput(
            attrs={'dir': 'auto'}
        )
    )
    company = forms.CharField(
        label=_('Company'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        )
    )
    number_of_staff = forms.ChoiceField(
        label=_('Current number of staff'),
        choices=EMPLOYEES,
        required=False,
    )
    sector = forms.ChoiceField(
        label=_('Sector'),
        choices=[],  # set in __init__
    )
    country = forms.ChoiceField(
        label=_('Country'),
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )

    expand = forms.BooleanField(
        label=_('Setting up a business in the UK'),
        required=False,
    )
    invest_capital = forms.BooleanField(
        label=_('Investing capital in the UK'),
        required=False,
    )
    buy_goods = forms.BooleanField(
        label=_('Buying goods from the UK'),
        required=False,
    )

    further_information = forms.BooleanField(
        label=_('I would like to receive further information')
    )
    terms_and_conditions = forms.BooleanField(
        label=_('I confirm the information provided is true and I accept DIT\'s terms and conditions')  # noqa
    )

    captcha = ReCaptchaField(label='', label_suffix='')
