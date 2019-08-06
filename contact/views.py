from directory_components.mixins import CountryDisplayMixin, GA360Mixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings

from contact import forms

from core.mixins import LocalisedURLsMixin, InvestEnableTranslationsMixin


class ActiveViewNameMixin:
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            active_view_name=self.active_view_name,
            *args,
            **kwargs
        )


class ContactFormView(
    ActiveViewNameMixin,
    InvestEnableTranslationsMixin,
    LocalisedURLsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    FormView,
):
    success_url = reverse_lazy('contact-success')
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm
    active_view_name = 'contact'
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
    ActiveViewNameMixin,
    LocalisedURLsMixin,
    InvestEnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView,
):
    template_name = 'contact/contact_form_success_page.html'
    active_view_name = 'contact'
    available_languages = settings.LANGUAGES

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestContactFormSuccess',
            business_unit='Invest',
            site_section='Contact',
            site_subsection='ContactSuccess'
        )
