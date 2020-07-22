from captcha.fields import ReCaptchaField
from directory_components import forms
from directory_constants import choices
from directory_forms_api_client.actions import GovNotifyEmailAction
from directory_forms_api_client.helpers import Sender

from django.conf import settings
from django.forms import Select, Textarea, SelectMultiple
from django.utils.translation import ugettext_lazy as _

from core import constants

HOW_DID_YOU_HEAR_CHOICES = [
    ('Advert in a publication', _('Advert in a publication')),
    ('Billboard or other outdoor advert', _('Billboard or other outdoor advert')),
    ('LinkedIn', _('LinkedIn')),
    ('Other social media', _('Other social media')),
    ('Internet search', _('Internet search')),
    ('Other', _('Other'))
]

HOW_CAN_WE_HELP_CHOICES = [
    (
        "I'm ready to invest and I'd like an adviser to call me.",
        _("I'm ready to invest and I'd like an adviser to call me."),
    ),
    (
        "I'm not quite ready to invest but I'd like to get updates on opportunities.",
        _("I'm not quite ready to invest but I'd like to get updates on opportunities."),
    ),
]


class HighPotentialOpportunityForm(forms.Form):
    action_class = GovNotifyEmailAction
    REQUIRED_USER_UTM_DATA_FIELD_NAMES = (
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_term',
        'utm_content',
    )

    def __init__(self, opportunity_choices, utm_data=None, *args, **kwargs):
        self.base_fields['opportunities'].choices = opportunity_choices
        self.utm_data = utm_data or {}
        # set empty string by default not exists data fields
        for field_name in self.REQUIRED_USER_UTM_DATA_FIELD_NAMES:
            self.utm_data.setdefault(field_name, '')
        return super().__init__(*args, **kwargs)

    given_name = forms.CharField(
        label=_('Given name')
    )
    family_name = forms.CharField(
        label=_('Family name')
    )
    job_title = forms.CharField(
        label=_('Job title')
    )
    email_address = forms.EmailField(
        label=_('Work email address')
    )
    phone_number = forms.CharField(
        label=_('Phone number')
    )
    company_name = forms.CharField(
        label=_('Company name')
    )
    website_url = forms.CharField(
        label=_('Company website')
    )
    company_address = forms.CharField(
        label=_('Company HQ address'),
        widget=Textarea()
    )
    country = forms.ChoiceField(
        label=_('Which country are you based in?'),
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    industry = forms.MultipleChoiceField(
        label=_('Your industry'),
        choices=choices.INDUSTRIES,
        widget=SelectMultiple()
    )
    opportunities = forms.MultipleChoiceField(
        label=_('Which opportunities are you interested in?'),
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=[]  # set in __init__
    )
    how_can_we_help = forms.ChoiceField(
        label=_('How can we help?'),
        choices=HOW_CAN_WE_HELP_CHOICES,
        widget=forms.RadioSelect(),
    )
    your_plans = forms.CharField(
        label=_('Tell us about your plans'),
        widget=Textarea()
    )
    how_did_you_hear = forms.ChoiceField(
        label=_('How did you hear about us?'),
        choices=HOW_DID_YOU_HEAR_CHOICES,
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

    @property
    def serialized_data(self):
        formatted_opportunities = [
            '• {opportunity[1]}: {opportunity[0]}'.format(opportunity=item)
            for item in self.base_fields['opportunities'].choices
            if item[0] in self.cleaned_data['opportunities']
        ]
        return {
            **self.cleaned_data,
            **self.utm_data,
            'opportunity_urls': '\n'.join(formatted_opportunities),
        }

    def send_agent_email(self, form_url, sender_ip_address):
        sender = Sender(
            email_address=self.cleaned_data['email_address'],
            country_code=self.cleaned_data['country'],
            ip_address=sender_ip_address,
        )
        action = self.action_class(
            template_id=settings.HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID,
            email_address=settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS,
            form_url=form_url,
            sender=sender,
        )
        response = action.save(self.serialized_data)
        response.raise_for_status()

    def send_user_email(self, form_url):
        # no need to set `sender` as this is just a confirmation email.
        action = self.action_class(
            template_id=settings.HPO_GOV_NOTIFY_USER_TEMPLATE_ID,
            email_address=self.cleaned_data['email_address'],
            form_url=form_url,
            email_reply_to_id=settings.HPO_GOV_NOTIFY_USER_REPLY_TO_ID,
        )
        response = action.save(self.serialized_data)
        response.raise_for_status()

    def save(self, form_url, sender_ip_address):
        self.send_agent_email(form_url=form_url, sender_ip_address=sender_ip_address)
        self.send_user_email(form_url=form_url)
