from captcha.fields import ReCaptchaField
from directory_components import forms
from directory_constants import choices, urls
from directory_forms_api_client.forms import ZendeskActionMixin
from directory_validators.url import not_contains_url_or_email
from directory_validators.string import no_html

from django.forms import Select, Textarea
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe

from core import constants


COMPANY = 'COMPANY'

COMPANY_CHOICES = (
    (COMPANY, _('Company')),
    ('OTHER', _('Other type of organisation')),
)


TERMS_LABEL = _(mark_safe(
    'Tick this box to accept the '
    f'<a class="link" href="{urls.domestic.TERMS_AND_CONDITIONS}" target="_blank">'
    'terms and conditions</a> of the great.gov.uk service.'
))


class SerializeMixin:
    def __init__(self, ingress_url, *args, **kwargs):
        self.ingress_url = ingress_url
        super().__init__(*args, **kwargs)

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        data['ingress_url'] = self.ingress_url
        del data['captcha']
        return data

    @property
    def full_name(self):
        assert self.is_valid()
        data = self.cleaned_data
        return f'{data["first_name"]} {data["last_name"]}'


class TransitionContactForm(SerializeMixin, ZendeskActionMixin, forms.Form):
    first_name = forms.CharField(label=_('Given name'))
    last_name = forms.CharField(label=_('Family name'))
    email = forms.EmailField(label=_('Email address'))
    organisation_type = forms.ChoiceField(
        label=_('Organisation type'),
        widget=forms.RadioSelect(),
        choices=COMPANY_CHOICES,
    )
    company_name = forms.CharField(label=_('Company name'))
    country = forms.ChoiceField(
        label=_('Which country are you based in?'),
        choices=[('', 'Please select')] + choices.COUNTRIES_AND_TERRITORIES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    city = forms.CharField(label=_('City'))
    comment = forms.CharField(
        label=_('Your question'),
        help_text=_("Please don't share commercially sensitive information."),
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
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
    )
