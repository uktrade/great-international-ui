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


class SectorPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    page_type = 'InternationalSectorPage'
    num_of_statistics = 0
    section_three_num_of_subsections = 0

    def count_data_with_field(self, list_of_data, field):
        filtered_list = [x for x in list_of_data if x[field]]
        return len(filtered_list)

    def get_context_data(self, **kwargs):
        context = super(SectorPageCMSView, self).get_context_data(**kwargs)
        self.num_of_statistics = \
            self.count_data_with_field(context['page']['statistics'], 'number')
        self.section_three_num_of_subsections = \
            self.count_data_with_field(
                context['page']['section_three_subsections'],
                'heading'
            )
        return context


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
