import logging

from directory_components.mixins import CountryDisplayMixin, EnableTranslationsMixin, GA360Mixin
from directory_constants import urls

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings

from second_qualification import forms
from core.header_config import tier_one_nav_items, tier_two_nav_items
from core.helpers import get_sender_ip_address
from core.mixins import InternationalHeaderMixin


logger = logging.getLogger(__name__)


class SecondQualificationFormView(
    InternationalHeaderMixin,
    EnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    FormView,
):
    success_url = reverse_lazy('second-qualification-success')
    template_name = 'second_qualification/form.html'
    form_class = forms.SecondQualificationForm
    available_languages = settings.LANGUAGES
    header_section = tier_one_nav_items.EXPAND
    header_sub_section = tier_two_nav_items.CONTACT_US_EXPAND

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='SecondQualificationForm',
            business_unit='Invest',
            site_section='Contact'
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['utm_data'] = self.request.utm
        kwargs['submission_url'] = self.request.path
        kwargs['emt_id'] = self.request.GET.get('emt_id')

        logger.warning("%s", kwargs)
        return kwargs

    def form_valid(self, form):
        form.save(sender_ip_address=get_sender_ip_address(self.request))
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            privacy_url=urls.domestic.PRIVACY_AND_COOKIES / 'fair-processing-notice-invest-in-great-britain/',
            emt_id=kwargs.get('emt_id'),
            *args, **kwargs)


class SecondQualificationSuccessView(
    InternationalHeaderMixin,
    EnableTranslationsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView,
):
    template_name = 'second_qualification/form_success.html'
    available_languages = settings.LANGUAGES
    header_section = tier_one_nav_items.EXPAND
    header_sub_section = tier_two_nav_items.CONTACT_US_EXPAND

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='SecondQualificationFormSuccess',
            business_unit='Invest',
            site_section='Contact',
            site_subsection='ContactSuccess'
        )
