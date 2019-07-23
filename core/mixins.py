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


TEMPLATE_MAPPING = {
    'InternationalHomePage': 'core/landing_page.html',
    'InternationalTopicLandingPage': 'core/topic_list.html',
    'InternationalArticleListingPage': 'core/article_list.html',
    'InternationalArticlePage': 'core/uk_setup_guide/article_detail.html',
    'InternationalCampaignPage': 'core/campaign.html',
    'InternationalSectorPage': 'core/sector_page.html',
    'InternationalSubSectorPage': 'core/sector_page.html',
    'InternationalCuratedTopicLandingPage': (
        'core/how_to_do_business_landing_page.html'),
    'InternationalGuideLandingPage': (
        'core/uk_setup_guide/guide_landing_page.html'),
    'InternationalEUExitFormPage': 'euexit/international-contact-form.html',
    'InternationalEUExitFormSuccessPage': (
        'euexit/international-contact-form-success.html'),
    'InternationalCapitalInvestLandingPage': (
        'core/capital_invest/capital_invest_landing_page.html'),
    'CapitalInvestRegionPage': (
        'core/capital_invest/capital_invest_region_page.html'),
    'CapitalInvestOpportunityPage': (
        'core/capital_invest/capital_invest_opportunity_page.html'),
    'CapitalInvestOpportunityListingPage': (
        'core/capital_invest/capital_invest_opportunity_listing_page.html'),
    'AboutDitServicesPage': 'core/about_dit/services_page.html',
    'AboutUkWhyChooseTheUkPage': 'core/about_uk/why_choose_the_uk_page.html',
    # Invest
    'InvestInternationalHomePage': 'invest/landing_page.html',
    'InvestHighPotentialOpportunityDetailPage': (
        'invest/high_potential_opportunity_detail.html'),
}

FEATURE_FLAGGED_URLS_MAPPING = {
    '/international/content/how-to-do-business-with-the-uk/': (
        'HOW_TO_DO_BUSINESS_ON'),
}


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):

        if self.request.path not in FEATURE_FLAGGED_URLS_MAPPING:
            return super().dispatch(*args, **kwargs)

        flag = FEATURE_FLAGGED_URLS_MAPPING.get(self.request.path, None)
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
        return TEMPLATE_MAPPING[self.page['page_type']]

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
