import directory_components.views
import directory_healthcheck.views

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap

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
    ),
    url(r'^international/i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
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
        r"^international/doing-business-with-the-uk/$",
        core.views.ArticleListPageView.as_view(),
        {'slug': 'doing-business-with-the-uk'},
        name="doing-business-with-the-uk"
    ),
    url(
        r"^international/industries/$",
        core.views.ArticleTopicPageView.as_view(),
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
    ),
    prefix_default_language=False,
)
