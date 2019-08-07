from directory_components.mixins import CountryDisplayMixin, GA360Mixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings

from contact import forms
from contact.mixins import LocalisedURLsMixin

from directory_components.mixins import EnableTranslationsMixin, InternationalHeaderMixin
from core.mixins import CMSPageFromSlugMixin


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
        form.save()
        return super().form_valid(form)


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

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestContactFormSuccess',
            business_unit='Invest',
            site_section='Contact',
            site_subsection='ContactSuccess'
        )


class CapitalInvestContactFormView(
    CMSPageFromSlugMixin,
    LocalisedURLsMixin,
    InternationalHeaderMixin,
    EnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    FormView,
):
    success_url = reverse_lazy('capital-invest-contact-success')
    slug = 'contact'
    page_type = 'CapitalInvestContactFormPage'
    template_name = 'core/capital_invest/capital_invest_contact_form.html'
    form_class = forms.CapitalInvestContactForm
    available_languages = settings.LANGUAGES

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='CapitalInvestContactForm',
            business_unit='CapitalInvest',
            site_section='Contact'
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['utm_data'] = self.request.utm
        kwargs['submission_url'] = self.request.path
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CapitalInvestContactFormSuccessView(
    LocalisedURLsMixin,
    InternationalHeaderMixin,
    EnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView,
):
    template_name = 'core/capital_invest/capital_invest_contact_form_success.html'
    available_languages = settings.LANGUAGES

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='CapitalInvestContactFormSuccess',
            business_unit='CapitalInvest',
            site_section='Contact',
            site_subsection='ContactSuccess'
        )
