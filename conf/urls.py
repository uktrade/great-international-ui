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
        core.views.CMSPageFromPathView.as_view(),
        {'path': 'international'},
        name="index"
    ),
    # avoid rendering the app root page
    url(
        r"^international/c/$",
        RedirectView.as_view(url=reverse_lazy('index')),
    ),
    # in case tree-based-routing is turned on for this page
    url(
        r"^international/c/international/$",
        RedirectView.as_view(url=reverse_lazy('index')),
    ),
    # hoping we can eliminate this one!
    url(
        r"^international/c/industries/$",
        core.views.CMSPageFromPathView.as_view(),
        {'path': 'industries'},
    ),
    url(
        r'^international/c/(?P<path>[\w\-/]*)$',
        core.views.CMSPageFromPathView.as_view(),
        name="render-cms-page"
    ),
)
