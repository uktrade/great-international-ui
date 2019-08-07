from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from directory_api_client.client import api_client
from directory_components.mixins import CountryDisplayMixin, GA360Mixin

from core.views import InternationalView
from find_a_supplier import forms


class AnonymousSubscribeFormView(CountryDisplayMixin, GA360Mixin, FormView):
    success_url = reverse_lazy('trade-subscribe-success')
    template_name = 'find_a_supplier/anonymous-subscribe.html'
    form_class = forms.AnonymousSubscribeForm

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierAnonymousSubscribeForm',
            business_unit='FindASupplier',
            site_section='AnonymousSubscribe',
            site_subsection='Form',
        )

    def form_valid(self, form):
        data = forms.serialize_anonymous_subscriber_forms(form.cleaned_data)
        response = api_client.buyer.send_form(data)
        response.raise_for_status()
        return super().form_valid(form)


class AnonymousSubscribeSuccessView(InternationalView):
    template_name = 'find_a_supplier/anonymous-subscribe-success.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierAnonymousSubscribeForm',
            business_unit='FindASupplier',
            site_section='AnonymousSubscribe',
            site_subsection='Success',
        )
