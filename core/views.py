from django.conf import settings
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response

from directory_constants import slugs, urls
from directory_constants.choices import COUNTRY_CHOICES
from directory_components.mixins import (
    CMSLanguageSwitcherMixin,
    GA360Mixin)
from directory_components.helpers import get_user_country
from directory_components.mixins import CountryDisplayMixin

from core.mixins import (
    TEMPLATE_MAPPING,
    GetSlugFromKwargsMixin,
    ArticleSocialLinksMixin,
    BreadcrumbsMixin,
    CMSPageMixin,
    RegionalContentMixin,
    HowToDoBusinessPageFeatureFlagMixin,
)
from core import forms


class BaseCMSPage(
    CMSLanguageSwitcherMixin,
    RegionalContentMixin,
    CMSPageMixin,
    GA360Mixin,
    TemplateView
):
    pass


class CampaignPageView(GetSlugFromKwargsMixin, BaseCMSPage):
    template_name = 'core/campaign.html'
    page_type = 'InternationalCampaignPage'
    ga360_payload = {'page_type': 'InternationalCampaignPage'}


class ArticleTopicPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalTopicLandingPage'
    ga360_payload = {'page_type': 'ArticleTopicPage'}


class ArticleListPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalArticleListingPage'
    ga360_payload = {'page_type': 'ArticleListPage'}


class LandingPageCMSView(BaseCMSPage):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    page_type = 'InternationalHomePage'
    slug = slugs.GREAT_HOME_INTERNATIONAL
    ga360_payload = {'page_type': 'InternationalHomePage'}

    tariffs_form_class = forms.TariffsCountryForm

    def get_context_data(self, *args, **kwargs):
        country_code = get_user_country(self.request)

        country_name = dict(COUNTRY_CHOICES).get(country_code, '')

        tariffs_country = {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }

        return super().get_context_data(
            tariffs_country=tariffs_country,
            tariffs_country_selector_form=self.tariffs_form_class(
                initial={'tariffs_country': country_code}),
            invest_contact_us_link=urls.INVEST_CONTACT_US,
            *args, **kwargs,
        )


class CuratedLandingPageCMSView(
    HowToDoBusinessPageFeatureFlagMixin, GetSlugFromKwargsMixin, BaseCMSPage
):
    active_view_name = 'curated-topic-landing'
    page_type = 'InternationalCuratedTopicLandingPage'
    ga360_payload = {'page_type': 'CuratedLandingPage'}


class GuideLandingPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    active_view_name = 'guide-landing'
    page_type = 'InternationalGuideLandingPage'
    ga360_payload = {'page_type': 'GuideLandingPage'}


class ArticlePageView(
    ArticleSocialLinksMixin, BreadcrumbsMixin,
    GetSlugFromKwargsMixin, BaseCMSPage,
):
    active_view_name = 'article'
    page_type = 'InternationalArticlePage'
    ga360_payload = {'page_type': 'ArticlePage'}


class IndustriesLandingPageCMSView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalTopicLandingPage'
    template_name = 'core/topic_list.html'
    ga360_payload = {'page_type': 'IndustriesLandingPage'}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        def rename_heading_field(page):
            page['landing_page_title'] = page['heading']
            return page

        context['page']['child_pages'] = [
            rename_heading_field(child_page)
            for child_page in context['page']['child_pages']]

        return context


class SectorPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    page_type = 'InternationalSectorPage'
    num_of_statistics = 0
    section_three_num_of_subsections = 0
    ga360_payload = {'page_type': 'SectorLandingPage'}

    def count_data_with_field(self, list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.num_of_statistics = self.count_data_with_field(
            context['page']['statistics'],
            'number'
        )
        self.section_three_num_of_subsections = self.count_data_with_field(
            context['page']['section_three_subsections'],
            'heading'
        )
        return context


class CMSPageFromPathView(
    BreadcrumbsMixin, CountryDisplayMixin, CMSLanguageSwitcherMixin,
    TemplateView
):
    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=settings.DIRECTORY_CMS_SITE_ID,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return self.handle_cms_response(response)

    def get_context_data(self, **kwargs):
        data = {'page': self.page}
        data.update(kwargs)
        return super().get_context_data(**data)

    def handle_cms_response(self, response):
        return handle_cms_response(response)

    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]
