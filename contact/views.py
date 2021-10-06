from directory_components.mixins import CountryDisplayMixin, EnableTranslationsMixin, GA360Mixin
from directory_constants import urls

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings

from contact import forms
from contact.mixins import LocalisedURLsMixin
from core.header_config import tier_one_nav_items
from core.helpers import get_sender_ip_address
from core.mixins import InternationalHeaderMixin


class ContactFormView(
    LocalisedURLsMixin,
    InternationalHeaderMixin,
    EnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    FormView,
):
    success_url = reverse_lazy('invest-contact-success')
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm
    available_languages = settings.LANGUAGES
    header_section = tier_one_nav_items.CONTACT

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestContactForm',
            business_unit='Invest',
            site_section='Contact'
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['utm_data'] = self.request.utm
        kwargs['submission_url'] = self.request.path
        return kwargs

    def form_valid(self, form):
        form.save(sender_ip_address=get_sender_ip_address(self.request))
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            privacy_url=urls.domestic.PRIVACY_AND_COOKIES / 'fair-processing-notice-invest-in-great-britain/',
            *args, **kwargs)


class ContactFormSuccessView(
    LocalisedURLsMixin,
    InternationalHeaderMixin,
    EnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView,
):
    template_name = 'contact/contact_form_success_page.html'
    available_languages = settings.LANGUAGES
    header_section = tier_one_nav_items.CONTACT

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestContactFormSuccess',
            business_unit='Invest',
            site_section='Contact',
            site_subsection='ContactSuccess'
        )
