from django.conf.urls import url

from core.views import QuerystringRedirectView


redirects_for_retired_pages_that_must_come_before_tree_based_routing = [
    # All of these can be used to discover which view code we need to delete
    url(
        # Redirect the old invest homepage to atlas
        r'^international/invest[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
    ),
    url(
        # Redirect the old capital invest homepage to atlas
        r'^international/content/capital-invest[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
    ),
    url(
        r'^international/content/capital-invest/how-we-help-you-invest-capital[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/'
        ),
    ),
    url(
        # Old CIOs
        r'^international/content/opportunities[/]*',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    url(
        # Old HPOs
        r'^international/content/invest/high-potential-opportunities[/]*',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    url(
        r'^international/content/about-us[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/'
        ),
    ),

    # How to expand UK setup
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/establish-a-base-for-business-in-the-uk/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/research-and-development-rd-support-in-the-uk/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/global-entrepreneur-program[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/global-entrepreneur-program/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/uk-visas-and-migration[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/uk-visas-and-migration/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/register-a-company-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/register-a-company-in-the-uk/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/hire-skilled-workers-for-your-uk-operations/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/open-a-uk-business-bank-account/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/uk-tax-and-incentives[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/uk-tax-and-incentives/'
        ),
    ),
    url(
        r'^international/content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/access-finance-in-the-uk/'
        ),
    ),

    url(
        # Redirect the rest of the 'invest' CMS page and all its tree-based children
        r'^international/content/invest/',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
    ),

    # About the UK was moved over to Why Invest in the UK
    url(
        r'^international/content/about-uk[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/'
        ),
    ),
    url(
        r'^international/content/about-uk/why-choose-uk[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/'
        ),
    ),
    url(
        r'^international/content/about-uk/why-choose-uk/tax-incentives[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/tax-incentives/'
        ),
    ),
    url(
        r'^international/content/about-uk/why-choose-uk/uk-talent-and-labour[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/uk-talent-and-labour/'
        ),
    ),
    url(
        r'^international/content/about-uk/why-choose-uk/uk-innovation[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/uk-innovation/'
        ),
    ),
    url(
        r'^international/content/about-uk/why-choose-uk/uk-infrastructure[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/uk-infrastructure/'
        ),
    ),
    url(
        r'^international/content/about-uk/industries[/]*',  # NB: wildcard
        QuerystringRedirectView.as_view(
            url='/international/content/investment/sectors/'
        ),
    ),
    url(
        r'^international/content/about-uk/regions[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/'
        ),
    ),
    url(
        r'^international/content/about-uk/regions/scotland[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/scotland/'
        ),
    ),

    url(
        r'^international/content/about-uk/regions/northern-ireland[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/northern-ireland/'
        ),
    ),

    url(
        r'^international/content/about-uk/regions/north-england[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/north-england/'
        ),
    ),

    url(
        r'^international/content/about-uk/regions/wales[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/wales/'
        ),
    ),

    url(
        r'^international/content/about-uk/regions/midlands[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/midlands/'
        ),
    ),

    url(
        r'^international/content/about-uk/regions/south-england[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/south-england/'
        ),
    ),
]


redirects_before_tree_based_routing_lookup = [
    # These ones are inserted into the urlconf before the 'cms-page-from-path' route is tried
    # so we can redirect pages that otherwise came from tree-based routing
    url(
        r'^international/content/opportunities[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    url(
        r'^international/content/invest/high-potential-opportunities/contact[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form'
        )
    ),
    url(
        r'^international/content/invest/high-potential-opportunities/contact/success[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form-success'
        )
    ),
    url(
        r'^international/content/expand/high-potential-opportunities/contact[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form'
        )
    ),
    url(
        r'^international/content/expand/high-potential-opportunities/contact/success[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form-success'
        )
    ),
] + redirects_for_retired_pages_that_must_come_before_tree_based_routing

redirects = [
    url(
        r'^international/eu-exit-news/contact[/]*$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form'),
    ),
    url(
        r'^international/eu-exit-news/contact/success[/]*$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form-success'),
    ),
    url(
        r'^international/brexit/contact[/]*$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form'),
    ),
    url(
        r'^international/brexit/contact/success[/]*$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form-success'),
    ),
]
