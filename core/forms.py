from directory_components import forms
from directory_forms_api_client.forms import GovNotifyEmailActionMixin
from django.forms import Select, Textarea, TextInput
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from directory_constants import urls

from django.utils.html import mark_safe
from directory_validators.url import not_contains_url_or_email
from directory_validators.string import no_html
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


from directory_constants.choices import COUNTRIES_AND_TERRITORIES, COUNTRY_CHOICES, INDUSTRIES

from django.conf import settings
from core import constants

COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES
INDUSTRY_OPTIONS = BLANK_CHOICE_DASH + list(INDUSTRIES)
COUNTRIES_AND_TERRITORIES = BLANK_CHOICE_DASH + COUNTRIES_AND_TERRITORIES


class TariffsCountryForm(forms.Form):
    tariffs_country = forms.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-tariffs-country-select'}),
        choices=COUNTRIES
    )


class OpportunitySearchForm(forms.Form):
    # NB: there is a specific version of this form for investment_atlas, which replaces this one

    sector = forms.ChoiceField(
        label='sector',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    scale = forms.ChoiceField(
        label='scale',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-scale'},
            use_nice_ids=True,
        ),
        required=False
    )
    region = forms.ChoiceField(
        label='region',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-region'},
            use_nice_ids=True,
        ),
        required=False
    )
    sub_sector = forms.ChoiceField(
        label='sub_sector',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sub_sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    sort_by = forms.ChoiceField(
        label='sort_by',
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
        widget=ReCaptchaV3()
    )
    email_contact_consent = forms.BooleanField(
        label=constants.EMAIL_CONSENT_LABEL,
        required=False
    )
    telephone_contact_consent = forms.BooleanField(
        label=constants.PHONE_CONSENT_LABEL,
        required=False
    )

    @property
    def serialized_data(self):
        # `captcha` is not useful to the agent so remove it from the submitted data.
        data = self.cleaned_data.copy()
        del data['captcha']
        return data


class BusinessEnvironmentGuideForm(GovNotifyEmailActionMixin, forms.Form):
    given_name = forms.CharField(label=_('Given name'), required=True)
    family_name = forms.CharField(label=_('Family name'), required=True)
    email_address = forms.EmailField(label=_('Email address'), required=True)
    phone_number = forms.CharField(label=_('Phone number'), required=True)
    market = forms.ChoiceField(
        label=_('What market are you in?'),
        choices=COUNTRIES_AND_TERRITORIES,
    )
    company_name = forms.CharField(label=_('Company name'), required=True)
    industry = forms.ChoiceField(
        label=_('Industry'),
        choices=INDUSTRY_OPTIONS,
        required=True,
    )
    email_contact_consent = forms.BooleanField(
        label=constants.EMAIL_CONSENT_LABEL,
        required=False
    )
    telephone_contact_consent = forms.BooleanField(
        label=constants.PHONE_CONSENT_LABEL,
        required=False
    )

    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        widget=ReCaptchaV3()
    )

    @property
    def serialized_data(self):
        # `captcha` is not useful to the agent so remove it from the submitted data.
        data = self.cleaned_data.copy()
        del data['captcha']
        return data


class WhyBuyFromUKFormNestedDetails(forms.Form):
    provide_more_info = forms.CharField(
        widget=Textarea,
        label=_('Tell us more about the type of products or services you’re interested in. '
                'The more you tell us, the quicker our response will be. (Optional)'),
        required=False,
    )


class WhyBuyFromUKForm(GovNotifyEmailActionMixin, forms.BindNestedFormMixin, forms.Form):
    given_name = forms.CharField(
        label=_('Given name'),
        error_messages={
            'required': _('Enter your full name'),
        }
    )
    family_name = forms.CharField(
        label=_('Family name'),
        error_messages={
            'required': _('Enter your full name'),
        }
    )
    email_address = forms.EmailField(
        label=_('Email address'),
        error_messages={
            'required': _(
                'Enter an email address in the correct format, like name@example.com'),
        }
    )
    company_name = forms.CharField(
        label=_('Company name'),
        error_messages={
            'required': _('Enter your company name'),
        }
    )
    job_title = forms.CharField(
        label=_('Job title (Optional)'),
        required=False
    )
    phone_number = forms.CharField(
        label=_('Phone number (Optional)'),
        required=False
    )
    city = forms.CharField(label=_('City (Optional)'), required=False,)

    market = forms.ChoiceField(
        label=_('What market are you in?'),
        choices=COUNTRIES_AND_TERRITORIES,
        error_messages={
            'required': _('Select a market'),
        }
    )

    procuring_products = forms.RadioNested(
        label=_('Are you interested in buying products or services from UK businesses, '
                'either now or in the near future?'),
        choices=(
            ('yes', _('Yes')),
            ('no', _('No')),
        ),
        nested_form_class=WhyBuyFromUKFormNestedDetails,
        nested_form_choice='yes',
        error_messages={
            'required': _('Select either yes or no'),
        }
    )

    industry = forms.ChoiceField(
        label=_('Your industry (optional)'),
        choices=INDUSTRY_OPTIONS,
        required=False,
    )
    contact_email = forms.BooleanField(
        label=constants.EMAIL_CONSENT_LABEL,
        required=False,
    )

    contact_phone = forms.BooleanField(
        label=constants.PHONE_CONSENT_LABEL,
        required=False,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        widget=ReCaptchaV3()
    )

    @property
    def serialized_data(self):
        # `captcha` is not useful to the agent so remove it from the submitted data.
        data = self.cleaned_data.copy()
        del data['captcha']
        return data


class InternationalRoutingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = self.get_international_choices()

    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=[],  # array overridden by constructor
    )

    def choice_is_enabled(self, value):
        flagged_choices = {
            constants.EXPORTING_TO_UK_CONTACT_URL: 'EXPORTING_TO_UK_ON',
            constants.CAPITAL_INVEST_CONTACT_URL: 'CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'
        }
        if value not in flagged_choices:
            return True

        return settings.FEATURE_FLAGS[flagged_choices[value]]

    def get_international_choices(self):
        all_choices = (
            (constants.INVEST_CONTACT_URL, _('Expanding to the UK')),
            (constants.CAPITAL_INVEST_CONTACT_URL, _('Investing capital in the UK')),
            (constants.EXPORTING_TO_UK_CONTACT_URL, _('Exporting to the UK')),
            (constants.BUYING_CONTACT_URL, _('Buying from the UK')),
            (constants.EUEXIT_CONTACT_URL, _('The transition period (now that the UK has left the EU)')),
            (constants.OTHER_CONTACT_URL, _('Other')),
        )
        return ((value, label) for value, label in all_choices if self.choice_is_enabled(value))
