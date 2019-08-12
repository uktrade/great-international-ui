from directory_components import forms
from django.forms import Select, Textarea, TextInput
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from directory_forms_api_client.actions import EmailAction
from directory_forms_api_client.helpers import Sender
from directory_constants import urls

from django.conf import settings
from django.template.loader import render_to_string
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
    f'<a class="link" href="{urls.TERMS_AND_CONDITIONS}" target="_blank">'
    'terms and conditions</a> of the great.gov.uk service.'
)


class CapitalInvestContactForm(forms.Form):
    action_class = EmailAction

    given_name = forms.CharField(label=_('Given name'), required=True)
    family_name = forms.CharField(label=_('Family name'), required=True)
    email = forms.EmailField(label=_('Email address'), required=True)
    phone_number = forms.CharField(
        label=_('Phone number (Optional)'),
        required=False,
        widget=TextInput(attrs={'type': 'tel'}))
    country = forms.ChoiceField(
        label=_('Which country are you based in?'),
        help_text=_(
            'We will use this information to put you in touch with '
            'your closest British embassy or high commission.'),
        choices=[('', '')] + COUNTRIES,
        widget=Select(attrs={'id': 'js-country-select'}), required=True
    )
    city = forms.CharField(label=_('City (Optional)'), required=False)
    message = forms.CharField(
        label=_('Message'),
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email],
        required=True
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        required=True
    )
    terms_agreed = forms.BooleanField(
        label=TERMS_LABEL,
        required=True
    )

    def __init__(self, utm_data, submission_url, *args, **kwargs):
        self.utm_data = utm_data
        self.submission_url = submission_url
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        data = self.cleaned_data.copy()
        return {
            'form_data': (
                (_('Given name'), data['given_name']),
                (_('Family name'), data['family_name']),
                (_('Email address'), data['email']),
                (_('Phone number'), data['phone_number']),
                (_('Country'), data['country']),
                (_('City'), data['city']),
                (_('Message'), data['message']),
            ),
            'utm': self.utm_data,
            'submission_url': self.submission_url,
        }

    def render_email(self, template_name):
        context = self.get_context_data()
        return render_to_string(template_name, context)

    def send_agent_email(self):
        sender = Sender(
            email_address=self.cleaned_data['email'],
            country_code=self.cleaned_data['country']
        )
        action = self.action_class(
            recipients=[settings.IIGB_AGENT_EMAIL, settings.CAPITAL_INVEST_CONTACT_EMAIL],
            subject='Capital Invest contact form lead',
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
            sender=sender,
        )
        response = action.save({
            'text_body': self.render_email('core/capital_invest/email/capital_invest_email_agent.txt'),
            'html_body': self.render_email('core/capital_invest/email/capital_invest_email_agent.html'),
        })
        response.raise_for_status()

    def send_user_email(self):
        # no need to set `sender` as this is just a confirmation email.
        action = self.action_class(
            recipients=[self.cleaned_data['email']],
            subject=str(_('Thank you for contacting us')),
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
        )
        response = action.save({
            'text_body': self.render_email('core/capital_invest/email/capital_invest_email_user.txt'),
            'html_body': self.render_email('core/capital_invest/email/capital_invest_email_user.html'),
        })
        response.raise_for_status()

    def save(self):
        self.send_agent_email()
        self.send_user_email()
