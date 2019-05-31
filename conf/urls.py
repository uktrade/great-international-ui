import directory_components.views
from directory_components.decorators import skip_ga360
import directory_healthcheck.views

from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.urls import reverse_lazy

import core.views
import conf.sitemaps
import euexit.views


sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
}


urlpatterns = [
    url(
        r'^international/healthcheck/',
        skip_ga360(directory_healthcheck.views.HealthcheckView.as_view()),
        name='healthcheck'
    ),
    url(
        r"^international/sitemap\.xml$",
        skip_ga360(sitemap),
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^international/robots\.txt$",
        skip_ga360(directory_components.views.RobotsView.as_view()),
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
        core.views.CMSPageFromPathView.as_view(),
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
