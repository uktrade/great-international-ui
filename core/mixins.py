from django.utils.functional import cached_property
from django.utils.cache import set_response_etag
from django.utils import translation
from django.http import Http404
from django.conf import settings

from directory_components.helpers import get_user_country
from directory_components.mixins import CountryDisplayMixin

from directory_constants.choices import EU_COUNTRIES
from directory_constants import cms

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response

from core import constants, helpers


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):

        if self.request.path not in constants.FEATURE_FLAGGED_URLS_MAPPING:
            return super().dispatch(*args, **kwargs)

        flag = constants.FEATURE_FLAGGED_URLS_MAPPING.get(self.request.path, None)
        flag_on = settings.FEATURE_FLAGS.get(flag, False)

        if not flag_on:
            raise Http404()

        return super().dispatch(*args, **kwargs)


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


class CMSPageFromSlugMixin:
    page_type = ''
    region = ''
    service_name = cms.GREAT_INTERNATIONAL

    @property
    def template_name(self):
        return constants.TEMPLATE_MAPPING[self.page['page_type']]

    def dispatch(self, request, *args, **kwargs):
        """
        Avoid showing the wrong page type at the wrong url

        e.g. /international/topic-slug should be a topic page
        this avoids /international/article-slug showing an article page
        at a url where it shouldn't exist
        """
        if self.page['page_type'] != self.page_type:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            service_name=self.service_name,
            region=self.region,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page, *args, **kwargs
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
