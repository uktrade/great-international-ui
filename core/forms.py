from directory_components import forms
from directory_forms_api_client.forms import GovNotifyEmailActionMixin
from django.forms import Select, Textarea, TextInput
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from directory_constants import urls

from django.utils.html import mark_safe
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html
from captcha.fields import ReCaptchaField


from directory_constants.choices import COUNTRY_CHOICES, EMPLOYEES, INDUSTRIES

from django.conf import settings
from core import constants

COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES
COMPANY_SIZE = BLANK_CHOICE_DASH + list(EMPLOYEES)
INDUSTRY_OPTIONS = BLANK_CHOICE_DASH + list(INDUSTRIES)


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


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    f'<a class="link" href="{urls.domestic.TERMS_AND_CONDITIONS}" target="_blank">'
    'terms and conditions</a> of the great.gov.uk service.'
)


class CapitalInvestContactForm(GovNotifyEmailActionMixin, forms.Form):

    given_name = forms.CharField(label=_('Given name'), required=True)
    family_name = forms.CharField(label=_('Family name'), required=True)
    email_address = forms.EmailField(label=_('Email address'), required=True)
    phone_number = forms.CharField(
        label=_('Phone number (Optional)'),
        required=False,
        widget=TextInput(attrs={'type': 'tel'}))
    country = forms.ChoiceField(
        label=_('Which country are you based in?'),
        choices=[('', '')] + COUNTRIES,
        widget=Select(attrs={'id': 'js-country-select'}), required=True
    )
    city = forms.CharField(label=_('City (Optional)'), required=False)
    company_name = forms.CharField(label=_('Company name (Optional)'), required=False)
    message = forms.CharField(
        label=_('Message'),
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email],
        required=True,
        help_text=_('How can we help?')
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        required=True
    )
    terms_agreed = forms.BooleanField(
        label=_(TERMS_LABEL),
        required=True
    )

    @property
    def serialized_data(self):
        # `captcha` and `terms_agreed` are not useful to agent
        # as those fields have to be present
        # for the form to be submitted.
        data = self.cleaned_data.copy()
        del data['captcha']
        del data['terms_agreed']
        return data


class BusinessEnvironmentGuideForm(GovNotifyEmailActionMixin, forms.Form):
    given_name = forms.CharField(label=_('Given name'), required=True)
    family_name = forms.CharField(label=_('Family name'), required=True)
    email_address = forms.EmailField(label=_('Email address'), required=True)
    company_name = forms.CharField(label=_('Company name (Optional)'), required=False)
    number_of_staff = forms.ChoiceField(
        label=_('Current number of staff (Optional)'),
        choices=COMPANY_SIZE,
        required=False,
    )
    industry = forms.ChoiceField(
        label=_('Industry'),
        choices=INDUSTRY_OPTIONS,
        required=True,
    )
    country = forms.ChoiceField(
        label=_('Country'),
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )

    mostly_interested_in = forms.MultipleChoiceField(
        label=_('I am mainly interested in:'),
        help_text=_('Select all that apply'),
        widget=forms.CheckboxSelectInlineLabelMultiple(),
        choices=(
            ('expand', _('Setting up a business in the UK')),
            ('invest_capital', _('Investing capital in the UK')),
            ('buy_goods', _('Buying good from the UK')),
        ),
        required=True
    )

    further_information = forms.BooleanField(
        label=_('I would like to receive further information'),
        required=False,
    )
    terms_agreed = forms.BooleanField(
        label=_('I confirm the information provided is true and I accept DIT\'s terms and conditions'),
        required=True,
    )

    captcha = ReCaptchaField(label='', label_suffix='')

    @property
    def serialized_data(self):
        # `captcha` and `terms_agreed` are not useful to the agent so remove them from the submitted data.
        data = self.cleaned_data.copy()
        del data['captcha']
        del data['terms_agreed']
        return data


def choice_is_enabled(value):
    flagged_choices = {
        constants.EXPORTING_TO_UK_CONTACT_URL: 'EXPORTING_TO_UK_ON',
        constants.CAPITAL_INVEST_CONTACT_URL: 'CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'
    }
    if value not in flagged_choices:
        return True

    return settings.FEATURE_FLAGS[flagged_choices[value]]


def international_choices():
    all_choices = (
        (constants.INVEST_CONTACT_URL, 'Investing in the UK'),
        (constants.CAPITAL_INVEST_CONTACT_URL, 'Capital investment in the UK'),
        (constants.EXPORTING_TO_UK_CONTACT_URL, 'Exporting to the UK'),
        (constants.BUYING_CONTACT_URL, 'Find a UK business partner'),
        (constants.EUEXIT_CONTACT_URL, 'Brexit enquiries'),
        (constants.OTHER_CONTACT_URL, 'Other'),
    )
    return ((value, label) for value, label in all_choices if choice_is_enabled(value))


class InternationalRoutingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = international_choices()

    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=[],  # array overridden by constructor
    )
