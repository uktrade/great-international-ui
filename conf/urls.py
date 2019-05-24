import directory_components.views
import directory_healthcheck.views

from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.urls import reverse_lazy

import core.views
import conf.sitemaps
import euexit.views


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
    url(
        r"^international/$",
        core.views.CMSPageFromPathView.as_view(),
        {'path': 'international/'},
        name="index"
    ),
    url(
        r'^international/content/$',
        RedirectView.as_view(url=reverse_lazy('index')),
        name="content-index-redirect"
    ),
    url(
        r"^international/contact/$",
        core.views.InternationalContactPageView.as_view(),
        name='contact-page-international'
    ),
    url(
        r'^international/eu-exit-news/contact/$',
        euexit.views.InternationalContactFormView.as_view(),
        name='eu-exit-international-contact-form'
    ),
    url(
        r'^international/eu-exit-news/contact/success/$',
        euexit.views.InternationalContactSuccessView.as_view(),
        name='eu-exit-international-contact-form-success'
    ),
    # these 3 named urls are required for breadcrumbs in templates
    url(
        r'^international/content/industries/$',
        core.views.CMSPageFromPathView.as_view(),
        {'path': 'industries'},
        name="industries"
    ),
    url(
        r"^international/content/how-to-setup-in-the-uk/$",
        core.views.CMSPageFromPathView.as_view(),
        {'path': 'how-to-setup-in-the-uk'},
        name="how-to-setup-in-the-uk"
    ),
    url(
        r"^international/content/how-to-do-business-with-the-uk/$",
        core.views.HowToDoBusinessWithTheUKView.as_view(),
        {'path': 'how-to-do-business-with-the-uk'},
        name="how-to-do-business-with-the-uk"
    ),
    # ----
    url(
        r'^international/content/(?P<path>[\w\-/]*)/$',
        core.views.CMSPageFromPathView.as_view(),
        name="cms-page-from-path"
    ),
    url(
        r'^international/content/(?P<path>[\w\-/]*)/(?P<list>[\w\-/]*)/$',
        core.views.CMSPageFromPathView.as_view(),
        name="cms-page-from-path-with-two-slugs"
    ),
]
