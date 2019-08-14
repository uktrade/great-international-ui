import directory_components.views
from directory_components.decorators import skip_ga360
import directory_healthcheck.views

from django.conf import settings
from django.conf.urls import url, include
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap

import core.views
from core.views import QuerystringRedirectView, DummyPage
import conf.sitemaps
import euexit.views
import invest.views
import contact.views


sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
}


urlpatterns = []


if settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON']:
    urlpatterns += [
        url(
            r'^international/investment-support-directory/',
            include(
                'investment_support_directory.urls',
                namespace='investment-support-directory',
            )
        ),
        url(
            r'^international/trade/investment-support-directory/search/',
            QuerystringRedirectView.as_view(url='/international/investment-support-directory/')
        ),
    ]


if settings.FEATURE_FLAGS['FIND_A_SUPPLIER_ON']:
    urlpatterns += [
        url(
            r'^international/trade/',
            include(
                'find_a_supplier.urls',
                namespace='find-a-supplier',
            )
        ),
        url(
            r'^international/content/trade/$',
            QuerystringRedirectView.as_view(pattern_name='trade-home'),
            name='content-trade-home-redirect'
        ),
    ]


urlpatterns += [
    url(
        r'^international/healthcheck/',
        skip_ga360(directory_healthcheck.views.HealthcheckView.as_view()),
        name='healthcheck'
    ),
    url(
        r'^international/sitemap\.xml$',
        skip_ga360(sitemap),
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r'^international/robots\.txt$',
        skip_ga360(directory_components.views.RobotsView.as_view()),
        name='robots'
    ),
    url(
        r'^international/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': '/'},
        name='index'
    ),
    url(
        r'^international/content/investment-support-directory/',
        DummyPage.as_view(),
        {
            'page-title': 'Investment Support Directory',
            'section': 'expand',
            'sub-section': 'investment-support-directory',
        },
        name='isd'
    ),
    url(
        r'^international/content/find-a-supplier/',
        DummyPage.as_view(),
        {
            'page-title': 'Find a UK Supplier',
            'section': 'trade',
            'sub-section': 'trade',
        },
        name='fas'
    ),
    url(
        r'^international/content/how-we-help-expand/',
        DummyPage.as_view(),
        {
            'page-title': 'How we help you to expand your business to the UK.',
            'section': 'expand',
            'sub-section': 'what-we-do',
        },
        name='fas'
    ),
    url(
        r'^international/content/how-we-help-trade/',
        DummyPage.as_view(),
        {
            'page-title': 'How we help you to trade with the UK.',
            'section': 'trade',
            'sub-section': 'what-we-do',
        },
        name='fas'
    ),
    url(
        r'^international/content/about-uk/regions/',
        DummyPage.as_view(),
        {
            'page-title': 'Regions of the UK',
            'section': 'expand',
            'sub-section': 'regions',
        },
    ),
    url(
        r'^international/content/about-uk/contact/',
        DummyPage.as_view(),
        {
            'page-title': 'Contact Us',
            'section': 'expand',
            'sub-section': 'contact',
        },
    ),
    url(
        r'^international/content/investment-types/',
        DummyPage.as_view(),
        {
            'page-title': 'Types of Investments',
            'section': 'invest',
            'sub-section': 'investment-types',
        },
    ),
    url(
        r'^international/content/how-to-invest-capital/',
        DummyPage.as_view(),
        {
            'page-title': 'How to Invest your Capital',
            'section': 'invest',
            'sub-section': 'how-to-invest-capital',
        },
    ),
    url(
        r'^international/content/capital-invest/contact/',
        DummyPage.as_view(),
        {
            'page-title': 'Contact Us',
            'section': 'invest',
            'sub-section': 'contact',
        },
    ),
    url(
        r'^international/content/how-to-buy/',
        DummyPage.as_view(),
        {
            'page-title': 'How to Buy from the UK',
            'section': 'trade',
            'sub-section': 'how-to-buy',
        },
    ),
    url(
        r'^international/content/how-we-help-trade/',
        DummyPage.as_view(),
        {
            'page-title': 'How we help you trade with the UK',
            'section': 'trade',
            'sub-section': 'how-we-help',
        },
    ),
    url(
        r'^international/content/trade/contact/',
        DummyPage.as_view(),
        {
            'page-title': 'Contact Us',
            'section': 'trade',
            'sub-section': 'contact',
        },
    ),
    url(
        r'^international/content/$',
        QuerystringRedirectView.as_view(pattern_name='index'),
        name='content-index-redirect'
    ),
    url(
        r'^international/invest/incoming/$',  # English homepage
        QuerystringRedirectView.as_view(pattern_name='invest-home'),
        name='invest-incoming-homepage'
    ),
    url(
        r'^international/invest/incoming/(?P<path>[\w\-/]*)/$',
        invest.views.LegacyInvestURLRedirectView.as_view(),
        name='invest-incoming'
    ),
    url(
        r'^international/invest/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': '/invest/'},
        name='invest-home'
    ),
    url(
        r"^international/invest/contact/$",
        contact.views.ContactFormView.as_view(),
        name="invest-contact"
    ),
    url(
        r"^international/invest/contact/success/$",
        contact.views.ContactFormSuccessView.as_view(),
        name="invest-contact-success"
    ),
    url(
        r'^international/content/invest/$',
        QuerystringRedirectView.as_view(pattern_name='invest-home'),
        name='content-invest-home-redirect'
    ),
    # Since we don't have a frontend page for the HPO landing page in the CMS
    # redirect to the HPO section on the homepage instead
    url(
        r'^international/content/invest/high-potential-opportunities/$',
        QuerystringRedirectView.as_view(
            url=('/international/content/invest/#high-potential-opportunities')),
        name='hpo-landing-page-redirect'
    ),
    url(
        r'^international/content/invest/high-potential-opportunities/contact/$',
        invest.views.HighPotentialOpportunityFormView.as_view(),
        {'path': '/invest/high-potential-opportunities/contact/'},
        name='high-potential-opportunity-request-form'
    ),
    url(
        r'^international/content/invest/high-potential-opportunities/contact/success/$',
        invest.views.HighPotentialOpportunitySuccessView.as_view(),
        {'path': '/invest/high-potential-opportunities/contact/success/'},
        name='high-potential-opportunity-request-form-success'
    ),
    url(
        r'^international/contact/$',
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
    url(
        r'^international/content/capital-invest/contact/$',
        core.views.CapitalInvestContactFormView.as_view(),
        {'path': '/capital-invest/contact/'},
        name='capital-invest-contact'
    ),
    # these next 3 named urls are required for breadcrumbs in templates
    url(
        r'^international/content/industries/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'industries'},
        name='industries'
    ),
    url(
        r'^international/content/how-to-setup-in-the-uk/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'how-to-setup-in-the-uk'},
        name='how-to-setup-in-the-uk'
    ),
    url(
        r'^international/content/how-to-do-business-with-the-uk/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'how-to-do-business-with-the-uk'},
        name='how-to-do-business-with-the-uk'
    ),
    url(
        r'^international/content/opportunities/$',
        core.views.OpportunitySearchView.as_view(),
        {'path': 'opportunities'},
        name='opportunities'
    ),
    url(
        r'^international/invest-capital/$',
        QuerystringRedirectView.as_view(url='/international/content/capital-invest/'),
        {'path': 'capital-invest'},
        name='invest-capital-home'
    ),
    url(
        r'^international/content/(?P<path>[\w\-/]*)/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        name='cms-page-from-path'
    ),
]

perfectfit = [
    url(
        r'^international/invest/perfectfit/',
        include(
            'perfect_fit_prospectus.urls',
            namespace='perfect_fit_prospectus'
        )
    ),
]

if settings.THUMBNAIL_STORAGE_CLASS_NAME == 'local-storage':
    urlpatterns += [
        url(
            r'^media/(?P<path>.*)$',
            skip_ga360(serve),
            {'document_root': settings.MEDIA_ROOT}
        ),
    ]

urlpatterns += perfectfit
