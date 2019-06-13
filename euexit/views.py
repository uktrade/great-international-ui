from directory_components.mixins import CountryDisplayMixin, GA360Mixin
from directory_constants import slugs
from directory_forms_api_client.helpers import Sender

from django.conf import settings
from django.urls import reverse_lazy
from django.utils import translation
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core.mixins import CMSPageMixin
from euexit import forms


SESSION_KEY_FORM_INGRESS_URL = 'FORM_INGRESS_URL'


class InternationalContactFormView(
    CMSPageMixin,
    CountryDisplayMixin,
    GA360Mixin,
    FormView,
):
    slug = slugs.EUEXIT_INTERNATIONAL_FORM
    form_class = forms.InternationalContactForm
    success_url = reverse_lazy('eu-exit-international-contact-form-success')
    subject = 'EU exit international contact form'
    page_type = 'InternationalEUExitFormPage'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id=self.page_type,
            business_unit='GreatInternational',
            site_section='EUExit',
            site_subsection='ContactForm'
        )

    def get(self, *args, **kwargs):
        translation.activate('en-gb')  # make sure header is in English
        self.request.session[SESSION_KEY_FORM_INGRESS_URL] = (
            self.request.META.get('HTTP_REFERER')
        )
        return super().get(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        kwargs['ingress_url'] = (
            self.request.session.get(SESSION_KEY_FORM_INGRESS_URL)
        )
        kwargs['disclaimer'] = self.page['disclaimer']
        return kwargs

    def form_valid(self, form):
        sender = Sender(
            email_address=form.cleaned_data['email'],
            country_code=form.cleaned_data.get('country_name'),
        )
        response = form.save(
            subject=self.subject,
            full_name=form.full_name,
            email_address=form.cleaned_data['email'],
            service_name='eu_exit',
            subdomain=settings.EU_EXIT_ZENDESK_SUBDOMAIN,
            form_url=self.request.path,
            sender=sender,
        )
        response.raise_for_status()
        return super().form_valid(form)


class InternationalContactSuccessView(CMSPageMixin, GA360Mixin, TemplateView):
    slug = slugs.EUEXIT_FORM_SUCCESS
    page_type = 'InternationalEUExitFormSuccessPage'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id=self.page_type,
            business_unit='GreatInternational',
            site_section='EUExit',
            site_subsection='ContactFormSuccess'
        )
