from directory_constants.constants import cms
from directory_cms_client.client import cms_api_client

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.urls import reverse
from django.utils.functional import cached_property

from directory_cms_client.helpers import handle_cms_response
from opportunities import forms
from core.views import CMSPageView
from core.mixins import GetSlugFromKwargsMixin


SESSION_KEY_SELECTED_OPPORTUNITIES = 'SELECTED_OPPORTUNITIES'


class HighPotentialOpportunityDetailView(
    GetSlugFromKwargsMixin,
    CMSPageView,
):
    active_view_name = 'high-potential-opportunity-detail'
    template_name = 'opportunities/high-potential-opportunity-detail.html'


class HighPotentialOpportunityFormView(FormView):
    template_name = 'opportunities/high-potential-opportunities-form.html'
    form_class = forms.HighPotentialOpportunityForm

    def get_success_url(self):
        return reverse(
            'high-potential-opportunity-request-form-success',
            kwargs={'slug': self.kwargs['slug']}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        kwargs['opportunity_choices'] = [
            (opportunity['pdf_document'], opportunity['heading'])
            for opportunity in self.page['opportunity_list']
        ]
        initial_opportunities_value = [
            item['pdf_document']
            for item in self.page['opportunity_list']
            if item['meta']['slug'] == self.kwargs['slug']
        ]
        kwargs['initial']['opportunities'] = initial_opportunities_value
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(page=self.page, **kwargs)

    def form_valid(self, form):
        form.save(form_url=self.request.path)
        self.request.session[SESSION_KEY_SELECTED_OPPORTUNITIES] = (
            form.cleaned_data['opportunities']
        )
        return super().form_valid(form)

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=cms.INVEST_HIGH_POTENTIAL_OPPORTUNITY_FORM_SLUG,
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        if response.status_code == 404:
            raise Http404()
        return handle_cms_response(response)


class HighPotentialOpportunitySuccessView(CMSPageView):
    template_name = 'opportunities/high-potential-opportunities-success.html'
    slug = cms.INVEST_HIGH_POTENTIAL_OPPORTUNITY_FORM_SUCCESS_SLUG
    active_view_name = 'high-potential-opportunity-form-success'

    def dispatch(self, *args, **kwargs):
        if SESSION_KEY_SELECTED_OPPORTUNITIES not in self.request.session:
            url = reverse(
                'high-potential-opportunity-request-form',
                kwargs={'slug': self.kwargs['slug']}
            )
            return redirect(url)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        selected_opportunites = self.request.session.pop(
            SESSION_KEY_SELECTED_OPPORTUNITIES
        )
        opportunities = [
            item for item in self.page['opportunity_list']
            if item['pdf_document'] in selected_opportunites
        ]

        return super().get_context_data(
            opportunities=opportunities,
            **kwargs
        )
