from django.forms import HiddenInput, Select, Textarea, TextInput, ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from directory_constants import choices, urls
from directory_components import forms
from directory_forms_api_client.forms import GovNotifyEmailActionMixin
from directory_validators.url import not_contains_url_or_email
from django.core.validators import EMPTY_VALUES
from django.db.models.fields import BLANK_CHOICE_DASH

from core import constants
from .constants import MARKETING_SOURCES

COMPANY_SIZE = BLANK_CHOICE_DASH + constants.EMPLOYEES
INDUSTRY_CHOICES = BLANK_CHOICE_DASH + list(choices.INDUSTRIES)


SELECT_LABEL = 'Please select your industry'


class SearchForm(forms.Form):

    q = forms.CharField(
        max_length=255,
        required=False,
    )
    industries = forms.ChoiceField(
        required=False,
        choices=(
            (('', _('All industries')),) + choices.INDUSTRIES
        ),
        widget=Select(attrs={'dir': 'ltr'})
    )


class CheckboxSelectMultipleIgnoreEmpty(forms.CheckboxSelectInlineLabelMultiple):

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        if values:
            return [value for value in values if value not in EMPTY_VALUES]


class CompanySearchForm(forms.Form):

    MESSAGE_MISSING_SECTOR_TERM = 'Please specify a search term or a sector.'

    q = forms.CharField(
        label='Search by product, service or company keyword',
        max_length=255,
        widget=TextInput(
            attrs={
                'placeholder': 'Search for UK suppliers',
                'autofocus': 'autofocus',
                'dir': 'auto',
                'data-ga-id': 'search-input',
                'value': '',
            }
        ),
        required=False,
    )
    page = forms.IntegerField(
        required=False,
        widget=HiddenInput,
        initial=1,
    )
    industries = forms.MultipleChoiceField(
        label='Industry expertise',
        widget=CheckboxSelectMultipleIgnoreEmpty(
            attrs={'id': 'checkbox-industry-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.INDUSTRIES,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('q') and not cleaned_data.get('industries'):
            raise ValidationError(self.MESSAGE_MISSING_SECTOR_TERM)
        return cleaned_data

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial


class ContactCompanyForm(GovNotifyEmailActionMixin, forms.Form):
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    TERMS_CONDITIONS_LABEL = (
        f'<p>I agree to the <a href="{urls.domestic.TERMS_AND_CONDITIONS}" '
        'class="link" target="_blank"> great.gov.uk terms and conditions </a> and I '
        'understand that:</p>'
        '<ul class="list list-bullet">'
        '<li>the Department for Business and Trade (DBT) is not endorsing'
        ' the character, ability, goods or services '
        'of members of the directory</li>'
        '<li>there is no legal relationship between DBT and directory members'
        '<li>DBT is not liable for any direct or indirect loss or damage '
        'that might happen after a directory member provides a good or '
        'service</li>'
        '</ul>'
    )
    given_name = forms.CharField(
        label='Given name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    family_name = forms.CharField(
        label='Family name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    company_name = forms.CharField(
        label='Your organisation name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    country = forms.CharField(
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    email_address = forms.EmailField(
        label='Your email address',
    )
    sector = forms.ChoiceField(
        label='Your industry',
        help_text='Please select your industry',
        choices=(
            [['', SELECT_LABEL]] + list(choices.INDUSTRIES)
        ),
    )
    subject = forms.CharField(
        label='Enter a subject line for your message',
        help_text='Maximum 200 characters.',
        max_length=200,
        validators=[not_contains_url_or_email],
    )
    body = forms.CharField(
        label='Enter your message to the UK company',
        help_text=(
            'Include the goods or services you’re interested in, and your '
            'country. Maximum 1000 characters.'
        ),
        max_length=1000,
        widget=Textarea,
        validators=[not_contains_url_or_email],
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        widget=ReCaptchaV3()
    )
    terms = forms.BooleanField(
        label=mark_safe(TERMS_CONDITIONS_LABEL),
        error_messages={'required': TERMS_CONDITIONS_MESSAGE},
    )
    marketing_consent = forms.BooleanField(
        label=constants.MARKETING_CONSENT_LABEL,
        required=False,
    )

    @property
    def serialized_data(self):
        data = super().serialized_data
        data['sector_label'] = dict(choices.INDUSTRIES)[data['sector']]
        return data


class SubscribeForm(forms.Form):
    PLEASE_SELECT_LABEL = _('Please select an industry')
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    TERMS_CONDITIONS_LABEL = mark_safe(
        f'<p>I agree to the <a class="link" href="{urls.domestic.TERMS_AND_CONDITIONS}" '
        'target="_blank"> great.gov.uk terms and conditions</a>.</p>'
    )

    full_name = forms.CharField(label=_('Your name'))
    email_address = forms.EmailField(label=_('Email address'))
    sector = forms.ChoiceField(
        label=_('Industry'),
        choices=(
            [['', PLEASE_SELECT_LABEL]] + list(choices.INDUSTRIES)
        ),
        widget=Select(attrs={'data-ga-id': 'sector-input'})
    )
    company_name = forms.CharField(label=_('Company name'))
    country = forms.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'data-ga-id': 'country-input'})
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        widget=ReCaptchaV3()
    )
    terms = forms.BooleanField(
        widget=forms.CheckboxWithInlineLabel(
            attrs={'class': 'visually-hidden-label'}
        ),
        label=TERMS_CONDITIONS_LABEL,
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )


def serialize_anonymous_subscriber_forms(cleaned_data):
    """
    Return the shape directory-api-client expects for saving international
    buyers.

    @param {dict} cleaned_data - All the fields in `SubscribeForm`
    @returns dict

    """

    return {
        'name': cleaned_data['full_name'],
        'email': cleaned_data['email_address'],
        'sector': cleaned_data['sector'],
        'company_name': cleaned_data['company_name'],
        'country': cleaned_data['country'],
    }


class BuyFromTheUKForm(GovNotifyEmailActionMixin, forms.Form):

    given_name = forms.CharField(
        label=_('Given name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    family_name = forms.CharField(
        label=_('Family name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    email_address = forms.EmailField(
        label=_('Email address'),
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    phone_number = forms.CharField(
        label=_('Phone number'),
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    sector = forms.ChoiceField(
        label=_('Your industry'),
        choices=INDUSTRY_CHOICES,
    )
    organisation_name = forms.CharField(
        label=_('Your organisation name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    organisation_size = forms.ChoiceField(
        label=_('Size of your organisation'),
        choices=COMPANY_SIZE,
        required=False,
    )
    country = forms.ChoiceField(
        label=_('Your country'),
        choices=[('', 'Please select')] + choices.COUNTRIES_AND_TERRITORIES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    body = forms.CharField(
        label=_('Describe what products or services you need'),
        help_text=_('Maximum 1000 characters.'),
        max_length=1000,
        widget=Textarea(
            attrs={'dir': 'auto'}
        ),
        validators=[not_contains_url_or_email],
    )
    source = forms.ChoiceField(
        label=_('Where did you hear about great.gov.uk?'),
        choices=(('', ''),) + MARKETING_SOURCES,
        required=False,
        initial=' ',  # prevent "other" being selected by default
        widget=Select(
            attrs={'class': 'js-field-other-selector'}
        )
    )
    source_other = forms.CharField(
        label=_("Other source (optional)"),
        required=False,
        widget=TextInput(
            attrs={
                'class': 'js-field-other',
                'dir': 'auto',
            }
        ),
        validators=[not_contains_url_or_email],
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
        # this data will be sent to zendesk. `captcha` and `terms_agreed` are
        # not useful to the zendesk user as those fields have to be present
        # for the form to be submitted.
        data = self.cleaned_data.copy()
        del data['captcha']
        data['country_name'] = dict(choices.COUNTRIES_AND_TERRITORIES)[data['country']]
        return data


class UnsubscribeForm(forms.Form):
    # not using EmailField because the value is signed
    uidb64 = forms.CharField(widget=HiddenInput)
    token = forms.CharField(widget=HiddenInput)
