import directory_components.views
import directory_healthcheck.views

from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

import core.views
import conf.sitemaps


sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
}


healthcheck_urls = [
    url(
        r'^sentry/$',
        directory_healthcheck.views.SentryHealthcheckView.as_view(),
        name='sentry'
    ),
    url(
        r'^forms-api/$',
        directory_healthcheck.views.FormsAPIBackendHealthcheckView.as_view(),
        name='forms-api'
    ),
]

urlpatterns = [
    url(
        r'^international/healthcheck/',
        include(
            healthcheck_urls, namespace='healthcheck', app_name='healthcheck'
        )
    ),
    url(
        r"^international/sitemap\.xml$", sitemap, {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^international/robots\.txt$",
        directory_components.views.RobotsView.as_view(),
        name='robots'
    )
]

urlpatterns += (
    url(
        r"^international/$",
        core.views.LandingPageCMSView.as_view(),
        name="index"
    ),
    url(
        r"^international/news/$",
        core.views.ArticleListPageView.as_view(),
        {'slug': 'news'},
        name="news"
    ),
    url(
        r"^international/how-to-do-business-with-the-uk/$",
        core.views.CuratedLandingPageCMSView.as_view(),
        {'slug': 'how-to-do-business-with-the-uk'},
        name="how-to-do-business-with-the-uk"
    ),
    url(
        r"^international/how-to-setup-in-the-uk/$",
        core.views.GuideLandingPageCMSView.as_view(),
        {'slug': 'how-to-setup-in-the-uk'},
        name="how-to-setup-in-the-uk"
    ),
    url(
        r"^international/how-to-do-business-with-the-uk/how-to-setup-in-the-uk/$",  # noqa
        RedirectView.as_view(url=reverse_lazy('how-to-setup-in-the-uk')),
    ),
    url(
        r"^international/how-to-setup-in-the-uk/guides/$",
        RedirectView.as_view(url='/international/how-to-setup-in-the-uk/#guides'), # noqa
    ),
    url(
        r"^international/industries/$",
        core.views.IndustriesLandingPageCMSView.as_view(),
        {'slug': 'industries'},
        name="industries"
    ),
    url(
        r"^international/industries/(?P<slug>[\w-]+)/$",
        core.views.SectorPageCMSView.as_view(),
        name="sector"
    ),
    url(
        r"^international/uk-setup-guide/$",
        core.views.SetupGuideLandingPageCMSView.as_view(),
        name="setup-guide"
    ),
    url(
        r"^international/uk-setup-guide/(?P<slug>[\w-]+)/$",
        core.views.SetupGuidePageCMSView.as_view(),
        name="guide-page"
    ),
    url(
        r"^international/uk-regions/(?P<slug>[\w-]+)/$",
        core.views.UKRegionPageCMSView.as_view(),
        name="uk-region"
    ),
    url(
        r"^international/campaigns/(?P<slug>[\w-]+)/$",
        core.views.CampaignPageView.as_view(),
        name="campaign"
    ),
    url(
        r"^international/(?P<slug>[\w-]+)/$",
        core.views.ArticleTopicPageView.as_view(),
        name="article-topic"
    ),
    url(
        r"^international/(?P<topic>[\w-]+)/(?P<slug>[\w-]+)/$",
        core.views.ArticleListPageView.as_view(),
        name="article-list"
    ),
    url(
        r"^international/(?P<topic>[\w-]+)/(?P<list>[\w-]+)/(?P<slug>[\w-]+)/$", # noqa
        core.views.ArticlePageView.as_view(),
        name="article-detail"
    )
)
