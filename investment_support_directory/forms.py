from captcha.fields import ReCaptchaField
from django.forms.widgets import HiddenInput, TextInput, Textarea
from django.utils.html import mark_safe

from directory_constants import choices, urls
from directory_components import forms
from directory_components.forms import fields, widgets
from directory_forms_api_client.forms import GovNotifyEmailActionMixin
from directory_validators.url import not_contains_url_or_email


class CompanyHomeSearchForm(forms.Form):

    q = fields.CharField(
        label='',
        max_length=255,
        required=False,
        widget=TextInput(
            attrs={
                'autofocus': 'autofocus',
                'dir': 'auto',
                'placeholder': 'Enter the name of the skills or service you’re looking for',
                'data-ga-id': 'search-input',
                'value': '',
            }
        ),
    )


class CompanySearchForm(forms.Form):

    MESSAGE_MINIMUM_VIABLE_SEARCH = (
        'Please specify a search term or expertise.'
    )

    q = fields.CharField(
        label='Search by product, service or company keyword',
        max_length=255,
        required=False,
        widget=TextInput(
            attrs={
                'placeholder': 'Search for UK suppliers',
                'autofocus': 'autofocus',
                'dir': 'auto',
                'data-ga-id': 'search-input'
            }
        ),
    )
    page = forms.IntegerField(
        required=False,
        widget=HiddenInput,
        initial=1,
    )
    expertise_industries = fields.MultipleChoiceField(
        label='Industry expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-industry-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.INDUSTRIES,
        required=False,
    )
    expertise_regions = fields.MultipleChoiceField(
        label='Regional expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-regional-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_REGION_CHOICES,
        required=False,
    )
    expertise_countries = fields.MultipleChoiceField(
        label='International expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-international-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.COUNTRY_CHOICES,
        required=False,
    )
    expertise_languages = fields.MultipleChoiceField(
        label='Language expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-language-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_LANGUAGES,
        required=False,
    )
    expertise_products_services_financial = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-expertise-products-services-financial'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_FINANCIAL,
        required=False,
    )
    expertise_products_services_management = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-management-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_MANAGEMENT_CONSULTING,
        required=False,
    )
    expertise_products_services_human_resources = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-human-expertise'},
            use_nice_ids=True,
        ),
        choices=[
            (value.replace(' ', '-'), label) for value, label in
            choices.EXPERTISE_HUMAN_RESOURCES
        ],
        required=False,
    )
    expertise_products_services_legal = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-legal-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_LEGAL,
        required=False,
    )
    expertise_products_services_publicity = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-publicity-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_PUBLICITY,
        required=False,
    )
    expertise_products_services_business_support = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-further-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_BUSINESS_SUPPORT,
        required=False,
    )

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial

    def clean(self):
        super().clean()
        # these field values are all stored in expertise_products_services, but
        # the form expresses them as separate fields for better user experience
        product_services_fields = [
            'expertise_products_services_financial',
            'expertise_products_services_management',
            'expertise_products_services_human_resources',
            'expertise_products_services_legal',
            'expertise_products_services_publicity',
            'expertise_products_services_business_support',
        ]
        labels = []
        for field_name in product_services_fields:
            if field_name in self.cleaned_data:
                labels += self.cleaned_data.get(field_name)
        self.cleaned_data['expertise_products_services_labels'] = labels

    def clean_expertise_products_services_human_resources(self):
        # Hack for AWS WAF 403 caused by spaces in 'on' within the querystring
        field = 'expertise_products_services_human_resources'
        return [item.replace('-', ' ') for item in self.cleaned_data[field]]


class ContactCompanyForm(GovNotifyEmailActionMixin, forms.Form):
    TERMS_CONDITIONS_LABEL = (
        f'<p>I agree to the <a href="{urls.domestic.TERMS_AND_CONDITIONS}" '
        'class="link" target="_blank"> great.gov.uk terms and conditions </a> and I '
        'understand that:</p>'
        '<ul class="list list-bullet">'
        '<li>the Department for International Trade (DIT) has reasonably '
        'tried to ensure that businesses listed in the UK Investment Support '
        'Directory are appropriately qualified and that the information in '
        'this directory is accurate and up to date</li>'
        '<li>DIT is not endorsing the character, ability, goods or services '
        'of members of the directory</li>'
        '<li>there is no legal relationship between DIT and directory '
        'members</li>'
        '<li>DIT is not liable for any direct or indirect loss or damage that '
        'might happen after a directory member provides a good or service</li>'
        '<li>directory members will give 1 hour’s free consultation to '
        'businesses that contact them through this service</li>'
        '</ul>'
    )
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    given_name = fields.CharField(
        label='Given name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    family_name = fields.CharField(
        label='Family name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    company_name = fields.CharField(
        label='Your organisation name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    email_address = fields.EmailField(
        label='Email address',
    )
    sector = fields.ChoiceField(
        label='Industry',
        choices=(
            [['', 'Please select your industry']] + list(choices.INDUSTRIES)
        ),
    )
    subject = fields.CharField(
        label='Enter a subject line for your message',
        max_length=200,
        validators=[not_contains_url_or_email],
    )
    body = fields.CharField(
        label='Enter your message to the UK company',
        help_text='Maximum 1000 characters.',
        max_length=1000,
        widget=Textarea,
        validators=[not_contains_url_or_email],
    )
    has_contact = fields.ChoiceField(
        label=(
            'Do you currently have a contact at Department for International '
            'Trade'
        ),
        widget=widgets.RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-one'}
        ),
        choices=(
            (True, 'Yes'),
            (False, 'No'),
        )
    )
    terms = fields.BooleanField(
        label=mark_safe(TERMS_CONDITIONS_LABEL),
        error_messages={'required': TERMS_CONDITIONS_MESSAGE},
    )
    captcha = ReCaptchaField(label='')
