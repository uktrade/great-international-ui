import logging

from directory_components import forms
from directory_forms_api_client.actions import EmailAction
from directory_forms_api_client.helpers import Sender

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


ARRANGE_CALLBACK_CHOICES = list((
    ('yes', _('Yes')),
    ('no', _('No'))
))


class SecondQualificationForm(forms.BindNestedFormMixin, forms.Form):
    action_class = EmailAction

    phone_number = forms.CharField(
        label=_('Phone number'),
    )
    arrange_callback = forms.ChoiceField(
        label=_('Would you like to arrange a call?'),
        choices=ARRANGE_CALLBACK_CHOICES,
        widget=forms.widgets.RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-one'}
        ),
    )
    emt_id = forms.CharField(
        label='emtid',
        label_suffix=''
    )

    def __init__(self, utm_data, submission_url, emt_id=None, *args, **kwargs):
        self.utm_data = utm_data
        self.submission_url = submission_url
        self.enquiry_id = emt_id
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        data = self.cleaned_data.copy()
        return {
            'form_data': (
                (_('Phone number'), data['phone_number']),
                (_('Would you like to arrange a call?'), data['arrange_callback']),
                (_('Enquiry ID'), data['emt_id']),
            ),
            'utm': self.utm_data,
            'submission_url': self.submission_url,
            'emt_id': self.enquiry_id,
        }

    def render_email(self, template_name):
        context = self.get_context_data()
        return render_to_string(template_name, context)

    def send_agent_email(self, sender_ip_address):
        sender = Sender(
            email_address="",
            ip_address=sender_ip_address,
        )
        action = self.action_class(
            recipients=[settings.IIGB_AGENT_EMAIL],
            subject='Second qualification form submission',
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
            sender=sender,
        )
        response = action.save({
            'text_body': self.render_email('email/email_agent.txt'),
            'html_body': self.render_email('email/email_agent.html'),
            'data': self.cleaned_data,
        })
        response.raise_for_status()

    def save(self, sender_ip_address):
        self.send_agent_email(sender_ip_address=sender_ip_address)
        logger.info("Second qualification form submitted for enquiry %s", self.data.get('emt_id'))
