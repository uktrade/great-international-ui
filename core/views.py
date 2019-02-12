from django.views.generic import TemplateView

from core.mixins import (
    GetSlugFromKwargsMixin,
    ArticleSocialLinksMixin,
    BreadcrumbsMixin,
    CMSPageMixin,
)
from directory_constants.constants import cms


class ArticleListPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, CMSPageMixin, TemplateView
):
    pass


class LandingPageCMSView(CMSPageMixin, TemplateView):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    slug = cms.EXPORT_READINESS_HOME_INTERNATIONAL_SLUG


class ArticlePageView(
    ArticleSocialLinksMixin, BreadcrumbsMixin, GetSlugFromKwargsMixin,
    CMSPageMixin, TemplateView
):
    active_view_name = 'article'
    template_name = 'core/article_detail.html'


class IndustriesLandingPageCMSView(CMSPageMixin, TemplateView):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'sector-landing-page'
    subpage_groups = ['children_sectors']


class IndustryPageCMSView(GetSlugFromKwargsMixin, CMSPageMixin, TemplateView):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']


class SetupGuideLandingPageCMSView(CMSPageMixin, TemplateView):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']


class SetupGuidePageCMSView(
    GetSlugFromKwargsMixin, CMSPageMixin, TemplateView
):
    active_view_name = 'setup-guide'
    template_name = 'core/accordion_content_page.html'


class UKRegionPageCMSView(GetSlugFromKwargsMixin, CMSPageMixin, TemplateView):
    template_name = 'core/accordion_content_page_with_hero_image.html'


class CampaignPageView(GetSlugFromKwargsMixin, CMSPageMixin, TemplateView):
    template_name = 'core/campaign.html'
