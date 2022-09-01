from django.utils.functional import cached_property
from django.utils.cache import set_response_etag

from directory_components.helpers import get_user_country
from directory_components.mixins import CountryDisplayMixin

from directory_constants.choices import EU_COUNTRIES

from core import helpers


class RegionalContentMixin(CountryDisplayMixin):
    """
    Extends CountryDisplayMixin to enable regional content
    """

    @property
    def region(self):
        country_code = get_user_country(self.request).upper() or None
        if country_code in EU_COUNTRIES:
            return 'eu'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            region=self.region,
            *args, **kwargs
        )


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class SubmitFormOnGetMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = self.request.GET or {}
        if data:
            kwargs['data'] = data
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CompanyProfileMixin:
    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])

    def get_context_data(self, **kwargs):
        company = helpers.CompanyParser(self.company)
        return super().get_context_data(
            company=company.serialize_for_template(),
            **kwargs
        )


class PersistSearchQuerystringMixin:

    @property
    def search_querystring(self):
        return self.request.GET.urlencode()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            search_querystring=self.search_querystring,
            **kwargs,
        )


class InternationalHeaderMixin:
    header_section = None
    header_sub_section = None

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            header_section=self.header_section.name if self.header_section else '',
            header_sub_section=self.header_sub_section.name if self.header_sub_section else '',
            *args,
            **kwargs
        )
