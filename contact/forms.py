from captcha.fields import ReCaptchaField
from directory_constants.choices import COUNTRY_CHOICES, INDUSTRIES
from directory_components import forms
from directory_forms_api_client.actions import EmailAction
from directory_forms_api_client.helpers import Sender
from django.db.models.fields import BLANK_CHOICE_DASH


from django.conf import settings
from django.forms import Textarea, Select
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES
INDUSTRY_CHOICES = BLANK_CHOICE_DASH + list(INDUSTRIES)
ARRANGE_CALLBACK_CHOICES = list((
    ('yes', _('Yes')),
    ('no', _('No'))
))

EXPANDING_TO_UK_CHOICES = BLANK_CHOICE_DASH + list((
    (
        'I’m convinced and want to talk to someone about my plans.',
        _('I’m convinced and want to talk to someone about my plans.')

    ),
    (
        'The UK is on my shortlist. How can the Department for International Trade help me?',
        _('The UK is on my shortlist. How can the Department for International Trade help me?')

    ),
    (
        'I’m still exploring where to expand my business and would like to know more about the UK’s offer.',
        _('I’m still exploring where to expand my business and would like to know more about the UK’s offer.')

    ),
    (
        'I’m not yet ready to invest. Keep me informed.',
        _('I’m not yet ready to invest. Keep me informed.')

    )
))


class ContactFormNestedDetails(forms.Form):
    when_to_call = forms.ChoiceField(
        label=_('When should we call you?'),
        choices=BLANK_CHOICE_DASH+list((
            (
                'in the morning',
                _('In the morning')
            ),
            (
                'in the afternoon',
                _('In the afternoon')
            ),
        )),
        required=False
    )


class ContactForm(forms.BindNestedFormMixin, forms.Form):
    action_class = EmailAction

    given_name = forms.CharField(label=_('Given name'))
    family_name = forms.CharField(label=_('Family name'))
    job_title = forms.CharField(label=_('Job title'))
    email = forms.EmailField(label=_('Work email address'))
    phone_number = forms.CharField(
        label=_('Phone number'),
    )
    company_name = forms.CharField(label=_('Company name'))
    company_website = forms.CharField(
        label=_('Company website'),
    )
    company_hq_address = forms.CharField(
        label=_('Company HQ address'),
    )
    country = forms.ChoiceField(
        label=_('Country'),
        choices=COUNTRIES,
        widget=Select(attrs={'id': 'js-country-select'})
    )
    industry = forms.ChoiceField(
        label=_('Industry'),
        choices=INDUSTRY_CHOICES
    )
    expanding_to_uk = forms.ChoiceField(
        label=_('Which of these best describes how you feel about expanding to the UK?'),
        choices=EXPANDING_TO_UK_CHOICES
    )
    description = forms.CharField(
        label=_('Tell us about your investment'),
        help_text=_(
            'Ask us any questions you might have or tell us your '
            'plans to expand to the UK, including size of the operation, '
            'why you’re considering the UK and what you’ll need to make it happen.'
            ),
        required=False,
        widget=Textarea()
    )
    arrange_callback = forms.RadioNested(
        label=_('Would you like us to arrange a call?'),
        choices=ARRANGE_CALLBACK_CHOICES,
        nested_form_class=ContactFormNestedDetails,
        nested_form_choice='yes',
    )
    email_contact_consent = forms.BooleanField(
        label=_('I would like to be contacted by email'),
        required=False
    )
    telephone_contact_consent = forms.BooleanField(
        label=_('I would like to be contacted by telephone'),
        required=False
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
                (_('Given name'), data['given_name']),
                (_('Family name'), data['family_name']),
                (_('Job title'), data['job_title']),
                (_('Work email address'), data['email']),
                (_('Phone number'), data['phone_number']),
                (_('Company name'), data['company_name']),
                (_('Company website'), data.get('company_website')),
                (_('Company HQ address'), data.get('company_hq_address')),
                (_('Country'), data['country']),
                (_('Industry'), data['industry']),
                (_('Which of these best describes how you feel about expanding to the UK?'), data['expanding_to_uk']),
                (_('Tell us about your investment'), data['description']),
                (_('Would you like us to arrange a call?'), data['arrange_callback']),
                (_('I would like to be contacted by email'), data['email_contact_consent']),
                (_('I would like to be contacted by telephone'), data['telephone_contact_consent']),
            ),
            'utm': self.utm_data,
            'submission_url': self.submission_url,
        }

    def render_email(self, template_name):
        context = self.get_context_data()
        return render_to_string(template_name, context)

    def send_agent_email(self, sender_ip_address):
        sender = Sender(
            email_address=self.cleaned_data['email'],
            country_code=self.cleaned_data['country'],
            ip_address=sender_ip_address,
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

    def save(self, sender_ip_address):
        self.send_agent_email(sender_ip_address=sender_ip_address)
        self.send_user_email()
