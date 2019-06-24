import directory_components.views
from directory_components.decorators import skip_ga360
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
        {'path': '/'},
        name="index"
    ),
    url(
        r'^international/invest/perfectfit/',
        include(
            'perfect_fit_prospectus.urls',
            namespace='perfect_fit_prospectus'
        )
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
    url(
        r"^international/content/opportunities/$",
        core.views.CMSPageFromPathView.as_view(),
        {'path': 'opportunities'},
        name="opportunities"
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
    url(
        r'^international/the-uk/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'About the UK',
            'header_area': 'about_uk'
        }
    ),
    url(
        r'^international/the-uk/regions/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank_regions.html",
            'title': 'UK regions',
            'header_area': 'about_uk'
        }
    ),
    url(
        r'^international/invest-capital/types/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank_investment_types.html",
            'title': 'Investment types',
            'header_area': 'capital_invest'
         }
    ),
    url(
        r'^international/invest-capital/types/venture-capital/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Venture capital',
            'header_area': 'capital_invest'
         }
    ),
    url(
        r'^international/invest-capital/types/invest-in-infrastructure/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Invest in infrastructure',
            'header_area': 'capital_invest'
         }
    ),
    url(
        r'^international/invest-capital/types/invest-in-energy/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Invest in energy',
            'header_area': 'capital_invest'
         }
    ),
    url(
        r'^international/invest-capital/types/invest-in-real-estate/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Invest in real estate',
            'header_area': 'capital_invest'
         }
    ),
    url(
        r'^international/invest-capital/opportunities/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Investment opportunities',
            'header_area': 'capital_invest'
        }
    ),
    url(
        r'^international/invest-capital/guides/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Investment guides',
            'header_area': 'capital_invest'
        }
    ),
    url(
        r'^international/import/guides/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Buying guides',
            'header_area': 'find_a_supplier'
        }
    ),
    url(
        r'^international/about-dit/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'About DIT',
            'header_area': 'about_dit'
        }
    ),
    url(
        r'^international/about-dit/case-studies/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'Success stories',
            'header_area': 'about_dit'
        }
    ),
    url(
        r'^international/latest/$',
        skip_ga360(core.views.BlankPage.as_view()),
        {
            'template': "core/blank.html",
            'title': 'News and events',
            'header_area': 'news_and_events'
        }
    )
]
