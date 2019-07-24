from captcha.fields import ReCaptchaField
from directory_components import forms
from directory_constants import choices, urls
from directory_forms_api_client.actions import GovNotifyAction
from directory_forms_api_client.helpers import Sender

from django.conf import settings
from django.forms import Select, Textarea
from django.utils.safestring import mark_safe


class HighPotentialOpportunityForm(forms.Form):
    action_class = GovNotifyAction
    COMPANY_SIZE_CHOICES = [
        ('1 - 10', '1 - 10'),
        ('11 - 50', '11 - 50'),
        ('51 - 250', '51 - 250'),
        ('250+', '250+'),
    ]
    REQUIRED_USER_UTM_DATA_FIELD_NAMES = (
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_term',
        'utm_content',
    )

    def __init__(
        self, field_attributes, opportunity_choices,
        utm_data=None, *args, **kwargs
    ):
        for field_name, field in self.base_fields.items():
            attributes = field_attributes.get(field_name)
            if attributes:
                field.__dict__.update(attributes)
        self.base_fields['opportunities'].choices = opportunity_choices
        self.utm_data = utm_data or {}
        # set empty string by default not exists data fields
        for field_name in self.REQUIRED_USER_UTM_DATA_FIELD_NAMES:
            self.utm_data.setdefault(field_name, '')
        return super().__init__(*args, **kwargs)

    full_name = forms.CharField()
    role_in_company = forms.CharField()
    email_address = forms.EmailField()
    phone_number = forms.CharField()
    company_name = forms.CharField()
    website_url = forms.CharField(required=False)
    country = forms.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    company_size = forms.ChoiceField(
        choices=COMPANY_SIZE_CHOICES
    )
    opportunities = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=[]  # set in __init__
    )
    comment = forms.CharField(
        widget=Textarea,
        required=False
    )
    terms_agreed = forms.BooleanField(
        label=mark_safe(
            'Tick this box to accept the '
            f'<a href="{urls.TERMS_AND_CONDITIONS}" target="_blank">terms and '
            'conditions</a> of the great.gov.uk service.'
        )
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

    def send_agent_email(self, form_url):
        sender = Sender(
            email_address=self.cleaned_data['email_address'],
            country_code=self.cleaned_data['country']
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

    def save(self, form_url):
        self.send_agent_email(form_url=form_url)
        self.send_user_email(form_url=form_url)
