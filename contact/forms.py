from captcha.fields import ReCaptchaField
from directory_constants import choices, urls
from directory_components import forms
from directory_forms_api_client.actions import EmailAction
from directory_forms_api_client.helpers import Sender

from django.conf import settings
from django.forms import Textarea, Select
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

COUNTRIES = [(label, label) for _, label in choices.COUNTRY_CHOICES]


STAFF_CHOICES = (
    (
        'Less than 10',
        _('Less than 10')
    ),
    (
        '10 to 50',
        _('10 to 50')
    ),
    (
        '51 to 250',
        _('51 to 250')
    ),
    (
        'More than 250',
        _('More than 250')
    ),
)


class ContactForm(forms.Form):
    action_class = EmailAction

    name = forms.CharField(label=_('Name'))
    job_title = forms.CharField(label=_('Job title'))
    email = forms.EmailField(label=_('Email address'))
    phone_number = forms.CharField(
        label=_('Phone number'),
        required=True
    )
    company_name = forms.CharField(label=_('Company name'))
    company_website = forms.CharField(
        label=_('Company website'),
        required=False
    )
    country = forms.ChoiceField(
        label=_('Which country are you based in?'),
        help_text=_(
            'We will use this information to put you in touch with '
            'your closest British embassy or high commission.'),
        choices=[('', '')] + COUNTRIES,
        widget=Select(attrs={'id': 'js-country-select'})
    )
    staff_number = forms.ChoiceField(
        label=_('Current number of staff'),
        choices=STAFF_CHOICES
    )
    description = forms.CharField(
        label=_('Tell us about your investment'),
        help_text=_(
            'Tell us about your company and your plans for the UK in '
            'terms of size of investment, operational and recruitment '
            'plans. Please also tell us what help you would like from '
            'the UK government.'
            ),
        widget=Textarea()
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )

    def __init__(self, utm_data, submission_url, *args, **kwargs):
        self.utm_data = utm_data
        self.submission_url = submission_url
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        data = self.cleaned_data.copy()

        return {
            'form_data': (
                (_('Name'), data['name']),
                (_('Email address'), data['email']),
                (_('Job title'), data['job_title']),
                (_('Phone number'), data['phone_number']),
                (_('Company name'), data['company_name']),
                (_('Company website'), data.get('company_website', '')),
                (_('Country'), data['country']),
                (_('Current number of staff'), data['staff_number']),
                (_('Your investment'), data['description'])
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
            recipients=[settings.IIGB_AGENT_EMAIL],
            subject='Contact form agent email subject',
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
            sender=sender,
        )
        response = action.save({
            'text_body': self.render_email('email/email_agent.txt'),
            'html_body': self.render_email('email/email_agent.html'),
        })
        response.raise_for_status()

    def send_user_email(self):
        # no need to set `sender` as this is just a confirmation email.
        action = self.action_class(
            recipients=[self.cleaned_data['email']],
            subject=str(_('Contact form user email subject')),
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
        )
        response = action.save({
            'text_body': self.render_email('email/email_user.txt'),
            'html_body': self.render_email('email/email_user.html'),
        })
        response.raise_for_status()

    def save(self):
        self.send_agent_email()
        self.send_user_email()
