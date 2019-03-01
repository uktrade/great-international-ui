from django.views.generic import TemplateView

from core.mixins import (
    GetSlugFromKwargsMixin,
    ArticleSocialLinksMixin,
    BreadcrumbsMixin,
    CMSPageMixin,
    RegionalContentMixin,
)
from directory_constants.constants import cms


class BaseCMSPage(RegionalContentMixin, CMSPageMixin, TemplateView):
    pass


class CampaignPageView(GetSlugFromKwargsMixin, BaseCMSPage):
    template_name = 'core/campaign.html'
    page_type = 'InternationalCampaignPage'


class ArticleTopicPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalTopicLandingPage'


class ArticleListPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalArticleListingPage'


class LandingPageCMSView(BaseCMSPage):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    page_type = 'InternationalHomePage'
    slug = cms.GREAT_HOME_INTERNATIONAL_SLUG


class ArticlePageView(
    ArticleSocialLinksMixin, BreadcrumbsMixin,
    GetSlugFromKwargsMixin, BaseCMSPage,
):
    active_view_name = 'article'
    page_type = 'InternationalArticlePage'


class IndustriesLandingPageCMSView(BaseCMSPage):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'sector-landing-page'
    subpage_groups = ['children_sectors']


class IndustryPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']


class SetupGuideLandingPageCMSView(BaseCMSPage):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']


class SetupGuidePageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    active_view_name = 'setup-guide'
    template_name = 'core/accordion_content_page.html'


class UKRegionPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    template_name = 'core/accordion_content_page_with_hero_image.html'
