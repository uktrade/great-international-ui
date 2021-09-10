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

sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
}

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
        # Note that some of these URLS from find-a-supplier are superceded by later
        # entries in the URLConf
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

# Must stay first so isn't changed by expand feature flag
urlpatterns += [
    url(
        r'^international/invest/incoming/(?P<path>[\w\-/]*)/$',
        invest.views.LegacyInvestURLRedirectView.as_view(),
        name='invest-incoming'
    ),
]

if settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON']:
    urlpatterns += [
        url(
            r'^international/invest/$',
            QuerystringRedirectView.as_view(pattern_name='expand-home'),
            name='invest-home-to-expand-home-redirect'
        ),
        url(
            r'^international/content/invest/$',
            QuerystringRedirectView.as_view(pattern_name='expand-home'),
            name='content-invest-to-expand-home-redirect'
        ),
        url(
            r'^international/invest/incoming/$',  # English homepage
            QuerystringRedirectView.as_view(pattern_name='expand-home'),
            name='invest-incoming-homepage'
        ),
        url(
            r'^international/invest/(?P<path>[\w\-/]*)/$',
            core.views.PathRedirectView.as_view(root_url='/international/expand'),
            name='invest-to-expand-redirect'
        ),
        url(
            r'^international/content/invest/(?P<path>[\w\-/]*)/$',
            core.views.PathRedirectView.as_view(root_url='/international/content/expand'),
            name='content-invest-to-expand-redirect'
        ),
    ]
    if settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON']:
        urlpatterns += [
            url(
                r'^international/content/how-to-setup-in-the-uk/$',
                QuerystringRedirectView.as_view(url='/international/content/expand/how-to-setup-in-the-uk/'),
                name='how-to-set-up-home-expand-redirect'
            ),
            url(
                r'^international/content/how-to-setup-in-the-uk/(?P<path>[\w\-/]*)/$',
                core.views.PathRedirectView.as_view(root_url='/international/content/expand/how-to-setup-in-the-uk'),
                name='how-to-set-up-expand-redirect'
            ),
        ]
elif not settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] and settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON']:
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
    # Could we remove the need for InternationalHomePageView by using MultilingualCMSPageFromPathView instead?
    # It seems InternationalHomePageView only sets the template, but this can be done in constants as for all
    # other pages...
    url(
        r'^international/$',
        core.views.InternationalHomePageView.as_view(),
        {'path': ''},
        name='index'
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
        r'^international/content/trade/contact/$',
        QuerystringRedirectView.as_view(pattern_name='find-a-supplier:industry-contact'),
        name='content-trade-contact-redirect'
    ),
    url(
        r'^international/invest/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'invest'},
        name='invest-home'
    ),
    url(
        r'^international/expand/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'expand'},
        name='expand-home'
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
        r'^international/content/invest/$',
        QuerystringRedirectView.as_view(pattern_name='invest-home'),
        name='content-invest-home-redirect'
    ),
    url(
        r'^international/content/expand/$',
        QuerystringRedirectView.as_view(pattern_name='expand-home'),
        name='content-expand-home-redirect'
    ),
    url(
        r'^trade/(?P<path>industries\/.*)/$',
        find_a_supplier.views.LegacySupplierURLRedirectView.as_view(),
    ),
    # These override at least one route from the find-a-supplier namespace, included far above
    url(
        r'^international/trade/incoming/$',  # Homepage
        QuerystringRedirectView.as_view(pattern_name='trade-home'),
        name='trade-incoming-homepage'
    ),
    url(
        r'^international/trade/incoming/(?P<path>[\w\-/]*)/$',
        find_a_supplier.views.LegacySupplierURLRedirectView.as_view(),
        name='trade-incoming'
    ),
    url(
        r'^international/trade/$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'trade'},
        name='trade-home'
    ),
    url(
        r'^international/content/trade/$',
        QuerystringRedirectView.as_view(pattern_name='trade-home'),
        name='content-trade-home-redirect'
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
        {'path': 'invest/high-potential-opportunities/contact'},
        name='high-potential-opportunity-request-form'
    ),
    url(
        r'^international/content/invest/high-potential-opportunities/contact/success/$',
        invest.views.HighPotentialOpportunitySuccessView.as_view(),
        {'path': 'invest/high-potential-opportunities/contact/success'},
        name='high-potential-opportunity-request-form-success'
    ),
    url(
        r'^international/content/expand/high-potential-opportunities/$',
        QuerystringRedirectView.as_view(
            url='/international/content/expand/#high-potential-opportunities'),
        name='hpo-landing-page-expand-redirect'
    ),
    url(
        r'^international/content/expand/high-potential-opportunities/contact/$',
        invest.views.HighPotentialOpportunityFormView.as_view(),
        {'path': 'expand/high-potential-opportunities/contact'},
        name='high-potential-opportunity-request-expand-form'
    ),
    url(
        r'^international/content/expand/high-potential-opportunities/contact/success/$',
        invest.views.HighPotentialOpportunitySuccessView.as_view(),
        {'path': 'expand/high-potential-opportunities/contact/success'},
        name='high-potential-opportunity-request-expand-form-success'
    ),
    url(
        r'^international/transition-period/contact/$',
        euexit.views.TransitionContactFormView.as_view(),
        name='brexit-international-contact-form'
    ),
    url(
        r'^international/transition-period/contact/success/$',
        euexit.views.InternationalContactSuccessView.as_view(),
        name='brexit-international-contact-form-success'
    ),
    url(
        r'^international/content/capital-invest/contact/$',
        core.views.CapitalInvestContactFormView.as_view(),
        {'path': 'capital-invest/contact'},
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
    # r'^international/content/opportunities/$', has been replaced by international/investment/opportunities/
    # and once the new investment atlas pages are live, we can remove all capinvest pages
    url(
        r'^international/invest-capital/$',
        QuerystringRedirectView.as_view(url='/international/content/capital-invest/'),
        {'path': 'capital-invest'},
        name='invest-capital-home'
    ),
    # The Investment Atlas section tries to stick with the standard
    # tree-based routing, apart from the investment root page at /international/investment/
    # and the filterable listing view at /international/investment/opportunities/
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
