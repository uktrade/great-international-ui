import directory_components.views
from directory_components.decorators import skip_ga360
import directory_healthcheck.views

from django.conf import settings
from django.conf.urls import url, include
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap

import core.views
from core.views import QuerystringRedirectView
import conf.sitemaps
from conf.url_redirects import (
    redirects,
    redirects_before_tree_based_routing_lookup
)
import euexit.views
import invest.views
import investment_atlas.views
import contact.views
import find_a_supplier.views
import second_qualification.views

# IMPORTANT: a lot of these views are no longer active - they are
# avoided by entries in redirects_before_tree_based_routing_lookup
# because they have been retired during the Investment Atlas refactor.
# Look at redirects_before_tree_based_routing_lookup in url_redirects.py
# to see which URL configs (and therefore views, and forms, and templates)
# we can actively drop from the codebase.

sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
}

# Investment Support Directory, Trade and Invest
urlpatterns = [
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
    url(
        r'^international/trade/',
        include(
            'find_a_supplier.urls',
            namespace='find-a-supplier',
        )
    ),
    url(
        r'^international/content/trade/$',
        QuerystringRedirectView.as_view(pattern_name='find-a-supplier:trade-home'),
        name='content-trade-home-redirect'
    ),
    url(
        r'^international/content/trade/contact/$',
        QuerystringRedirectView.as_view(pattern_name='find-a-supplier:industry-contact'),
        name='content-trade-contact-redirect'
    ),
    url(
        r'^international/trade/incoming/$',
        QuerystringRedirectView.as_view(pattern_name='find-a-supplier:trade-home'),
        name='trade-incoming-homepage'
    ),
    # This entry handles all URLs in find_a_supplier/redirects.py
    url(
        r'^international/trade/incoming/(?P<path>[\w\-/]*)/$',
        find_a_supplier.views.LegacySupplierURLRedirectView.as_view(),
        name='trade-incoming'
    ),
    # This entry handles all URLs in invest/redirects.py
    url(
        r'^international/invest/incoming/(?P<path>[\w\-/]*)/$',
        invest.views.LegacyInvestURLRedirectView.as_view(),
        name='invest-incoming'
    ),
]

if settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON']:
    urlpatterns += [
        url(
            r'^international/content/how-to-setup-in-the-uk/$',
            QuerystringRedirectView.as_view(url='/international/content/invest/how-to-setup-in-the-uk/'),
            name='how-to-set-up-home-invest-redirect'
        ),
        url(
            r'^international/content/how-to-setup-in-the-uk/(?P<path>[\w\-/]*)/$',
            core.views.PathRedirectView.as_view(root_url='/international/content/invest/how-to-setup-in-the-uk'),
            name='how-to-set-up-invest-redirect'
        ),
    ]

urlpatterns += [
    url(
        r'^international/content/industries/advanced-manufacturing/$',
        QuerystringRedirectView.as_view(url='/international/content/industries/engineering-and-manufacturing/'),
        name='advanced-manufacturing-redirect'
    )
]

if settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON']:
    urlpatterns += [
        url(
            r'^international/content/industries/$',
            QuerystringRedirectView.as_view(url='/international/content/about-uk/industries/'),
            name='industries-home-to-about-uk-redirect'
        ),
        url(
            r'^international/content/industries/(?P<path>[\w\-/]*)/$',
            core.views.PathRedirectView.as_view(root_url='/international/content/about-uk/industries'),
            name='industries-to-about-uk-redirect'
        ),
    ]

# This route remains in use after the Atlas refactor
if settings.FEATURE_FLAGS['INTERNATIONAL_TRIAGE_ON']:
    urlpatterns += [
        url(
            r'^international/contact/$',
            core.views.InternationalContactTriageView.as_view(),
            name='international-contact-triage'
        ),
    ]
else:
    urlpatterns += [
        url(
            r'^international/contact/$',
            core.views.InternationalContactPageView.as_view(),
            name='contact-page-international'
        ),
    ]

urlpatterns += [
    url(
        r'international/invest/request-call/$',
        second_qualification.views.SecondQualificationFormView.as_view(),
        name="second-qualification"
    ),
    url(
        r'international/invest/request-call/success/$',
        second_qualification.views.SecondQualificationSuccessView.as_view(),
        name="second-qualification-success"
    ),
]

urlpatterns += redirects_before_tree_based_routing_lookup

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
        {'path': ''},
        name='index'
    ),
    url(
        r'^international/content/$',
        QuerystringRedirectView.as_view(pattern_name='index'),
        name='content-index-redirect'
    ),
    url(
        r'^international/invest/incoming/$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
        name='invest-incoming-homepage'
    ),
    url(
        r'^international/expand/$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
        name='expand-homepage-redirect'
    ),
    url(
        # Remains in use after the Atlas refactor
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
        r"^international/expand/contact/$",
        contact.views.ContactFormView.as_view(),
        name="expand-contact"
    ),
    url(
        r"^international/expand/contact/success/$",
        contact.views.ContactFormSuccessView.as_view(),
        name="expand-contact-success"
    ),
    url(
        r'^international/content/expand/$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
        name='content-expand-home-redirect'
    ),
    url(
        r'^trade/(?P<path>industries\/.*)/$',
        find_a_supplier.views.LegacySupplierURLRedirectView.as_view(),
    ),
    url(
        r'^international/content/expand/high-potential-opportunities/$',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
        name='hpo-landing-page-expand-redirect'
    ),
    url(
        # Remains in use after the Atlas refactor
        r'^international/transition-period/contact/$',
        euexit.views.TransitionContactFormView.as_view(),
        name='brexit-international-contact-form'
    ),
    url(
        # Remains in use after the Atlas refactor
        r'^international/transition-period/contact/success/$',
        euexit.views.InternationalContactSuccessView.as_view(),
        name='brexit-international-contact-form-success'
    ),
    url(
        r'^international/content/investment/contact/$',
        core.views.CapitalInvestContactFormView.as_view(),
        {'path': 'investment/contact'},
        name='investment-contact'
    ),
    url(
        r'^international/invest-capital/$',
        QuerystringRedirectView.as_view(url='/international/content/capital-invest/'),
        {'path': 'capital-invest'},
        name='invest-capital-home'
    ),
    # The Investment Atlas section tries to stick with the standard
    # tree-based routing, apart from:
    #   * the investment root page at /international/investment/
    #   * the filterable listing view at /international/investment/opportunities/
    #   * a special FDI contact form
    #
    # NOTE: the rest of the alas pages will be served by the "cms-page-from-path" view,
    # declared later in this file as /international/content/investment/child-slug/grandchild-slug/
    #
    url(
        r'^international/investment/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {
            'path': 'investment'
            # ie, in the CMS there must a direct child of the International homepage with the slug of 'investment'
        },
        name='atlas-home'
    ),
    url(
        r'^international/investment/opportunities/$',
        investment_atlas.views.InvestmentOpportunitySearchView.as_view(),
        {
            'path': 'investment/opportunities/'
        },
        name='atlas-opportunities'
    ),
    url(
        r'^international/content/investment/foreign-direct-investment-contact/$',
        investment_atlas.views.ForeignDirectInvestmentOpportunityFormView.as_view(),
        {'path': 'investment/foreign-direct-investment-contact'},
        name='fdi-opportunity-request-form'
    ),
    url(
        r'^international/content/investment/foreign-direct-investment-contact/success/$',
        investment_atlas.views.ForeignDirectInvestmentOpportunitySuccessView.as_view(),
        {'path': 'investment/foreign-direct-investment-contact/success'},
        name='fdi-opportunity-request-form-success'
    ),
    url(
        # This view is crucial to the CMS pages that use tree-based-routing - they seem to all use it.
        # Also see core.constants.TEMPLATE_MAPPING for how a paritcular CMS page model in directory-cms
        # is mapped to HTML template in great-international-ui
        r'^international/content/(?P<path>[\w\-/]*)/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        name='cms-page-from-path'
    ),
    url(
        r"^international/trade/how-we-help-you-buy/why-buy-from-the-uk/$",
        core.views.WhyBuyFromUKFormView.as_view(),
        name='why-buy-from-uk-form'
    ),
    url(
        r"^international/trade/how-we-help-you-buy/why-buy-from-the-uk/success/$",
        core.views.WhyBuyFromUKFormViewSuccess.as_view(),
        name='why-buy-from-uk-form-success'
    ),
]

if settings.FEATURE_FLAGS['GUIDE_TO_BUSINESS_ENVIRONMENT_FORM_ON']:
    urlpatterns += [
        url(
            r"^international/about-uk/why-choose-uk/business-environment-guide/$",
            core.views.BusinessEnvironmentGuideFormView.as_view(),
            name='business-environment-guide-form'
        ),
        url(
            r"^international/about-uk/why-choose-uk/business-environment-guide/success/$",
            core.views.BusinessEnvironmentGuideFormSuccessView.as_view(),
            name='business-environment-guide-form-success'
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
urlpatterns += redirects

handler404 = core.views.handler404
handler500 = core.views.handler500
