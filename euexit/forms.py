from captcha.fields import ReCaptchaField
from directory_components import forms, fields, widgets
from directory_constants import choices, urls
from directory_forms_api_client.forms import ZendeskActionMixin
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html

from django.forms import Select, Textarea
from django.utils.html import mark_safe


COMPANY = 'COMPANY'

COMPANY_CHOICES = (
    (COMPANY, 'Company'),
    ('OTHER', 'Other type of organisation'),
)


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    f'<a class="link" href="{urls.TERMS_AND_CONDITIONS}" target="_blank">terms and '
    'conditions</a> of the great.gov.uk service.'
)


class FieldsMutationMixin:
    def __init__(self, field_attributes, disclaimer, *args, **kwargs):
        for field_name, field in self.base_fields.items():
            attributes = field_attributes.get(field_name)
            if attributes:
                field.__dict__.update(attributes)
        super().__init__(*args, **kwargs)
        widget = self.fields['terms_agreed'].widget
        widget.label = mark_safe(f'{widget.label}  {disclaimer}')


class SerializeMixin:
    def __init__(self, ingress_url, *args, **kwargs):
        self.ingress_url = ingress_url
        super().__init__(*args, **kwargs)

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        data['ingress_url'] = self.ingress_url
        del data['captcha']
        del data['terms_agreed']
        return data

    @property
    def full_name(self):
        assert self.is_valid()
        data = self.cleaned_data
        return f'{data["first_name"]} {data["last_name"]}'


class InternationalContactForm(
    FieldsMutationMixin, SerializeMixin, ZendeskActionMixin, forms.Form
):
    first_name = fields.CharField()
    last_name = fields.CharField()
    email = fields.EmailField()
    organisation_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_CHOICES,
    )
    company_name = fields.CharField()
    country = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    city = fields.CharField()
    comment = fields.CharField(
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )
