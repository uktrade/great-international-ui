from django.views.generic import TemplateView

from directory_constants import slugs, cms
from directory_components.mixins import GA360Mixin, CMSLanguageSwitcherMixin

from core.mixins import CMSPageFromSlugMixin


class InvestCMSPageFromSlugView(
    CMSPageFromSlugMixin,
    CMSLanguageSwitcherMixin,
    GA360Mixin,
    TemplateView
):
    service_name = cms.INVEST


class InvestHomePage(InvestCMSPageFromSlugView):
    page_type = 'InvestHomePage'
    slug = slugs.INVEST_HOME_PAGE
