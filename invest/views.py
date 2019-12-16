from directory_components.mixins import GA360Mixin
from directory_constants import slugs
from django.conf import settings

from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy

from . import helpers, forms, redirects
from core.views import MonolingualCMSPageFromPathView, LegacyRedirectCoreView

SESSION_KEY_SELECTED_OPPORTUNITIES = 'SELECTED_OPPORTUNITIES'


class HighPotentialOpportunityFormView(MonolingualCMSPageFromPathView, GA360Mixin, FormView):
    template_name = 'invest/hpo/high_potential_opportunities_form.html'
    form_class = forms.HighPotentialOpportunityForm
    success_url = reverse_lazy('high-potential-opportunity-request-form-success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        kwargs['opportunity_choices'] = [
            (opportunity['pdf_document'], opportunity['heading'])
            for opportunity in self.page['opportunity_list']
        ]
        kwargs['utm_data'] = self.request.utm
        return kwargs

    def form_valid(self, form):
        form.save(form_url=self.request.path)
        self.request.session[SESSION_KEY_SELECTED_OPPORTUNITIES] = (
            form.cleaned_data['opportunities']
        )
        return super().form_valid(form)


class HighPotentialOpportunitySuccessView(MonolingualCMSPageFromPathView):
    template_name = 'invest/hpo/high_potential_opportunities_form_success.html'
    slug = slugs.INVEST_HIGH_POTENTIAL_OPPORTUNITY_FORM_SUCCESS

    def dispatch(self, *args, **kwargs):
        if SESSION_KEY_SELECTED_OPPORTUNITIES not in self.request.session:
            return redirect(
                reverse('high-potential-opportunity-request-form'))
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


class LegacyInvestURLRedirectView(LegacyRedirectCoreView):
    redirects_mapping = redirects.REDIRECTS
    fallback_url = '/international/invest/'

    @staticmethod
    def translate_language_from_path_to_querystring(path, params):
        if path.startswith(helpers.LANGUAGE_CODES):
            lang = helpers.get_language_from_prefix(path)
            path = path[len(lang) + 1:]  # +1 is for the /
            if lang not in settings.INVEST_REDIRECTS_UNUSED_LANGUAGES:  # these go to English
                params['lang'] = lang
        return path, params

