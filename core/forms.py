from directory_components import forms
from directory_forms_api_client.forms import GovNotifyActionMixin
from django.forms import Select, Textarea, TextInput
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from directory_constants import urls

from django.utils.html import mark_safe
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html
from captcha.fields import ReCaptchaField


from directory_constants.choices import COUNTRY_CHOICES


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


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    f'<a class="link" href="{urls.domestic.TERMS_AND_CONDITIONS}" target="_blank">'
    'terms and conditions</a> of the great.gov.uk service.'
)


class CapitalInvestContactForm(GovNotifyActionMixin, forms.Form):

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
