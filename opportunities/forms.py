from captcha.fields import ReCaptchaField
from directory_components import forms, fields, widgets
from directory_constants.constants import choices, urls
from directory_forms_api_client.actions import GovNotifyAction

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

    def __init__(
        self, field_attributes, opportunity_choices, *args, **kwargs
    ):
        for field_name, field in self.base_fields.items():
            attributes = field_attributes.get(field_name)
            if attributes:
                field.__dict__.update(attributes)
        self.base_fields['opportunities'].choices = opportunity_choices
        return super().__init__(*args, **kwargs)

    full_name = fields.CharField()
    role_in_company = fields.CharField()
    email_address = fields.EmailField()
    phone_number = fields.CharField()
    company_name = fields.CharField()
    website_url = fields.CharField(required=False)
    country = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    company_size = fields.ChoiceField(
        choices=COMPANY_SIZE_CHOICES
    )
    opportunities = fields.MultipleChoiceField(
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=[]  # set in __init__
    )
    comment = fields.CharField(
        widget=Textarea,
        required=False
    )
    terms_agreed = fields.BooleanField(
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
            'opportunity_urls': '\n'.join(formatted_opportunities),
        }

    def send_agent_email(self, form_url):
        action = self.action_class(
            template_id=settings.HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID,
            email_address=settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS,
            form_url=form_url,
        )
        response = action.save(self.serialized_data)
        response.raise_for_status()

    def send_user_email(self, form_url):
        action = self.action_class(
            template_id=settings.HPO_GOV_NOTIFY_USER_TEMPLATE_ID,
            email_address=self.cleaned_data['email_address'],
            form_url=form_url,
        )
        response = action.save(self.serialized_data)
        response.raise_for_status()

    def save(self, form_url):
        self.send_agent_email(form_url=form_url)
        self.send_user_email(form_url=form_url)
