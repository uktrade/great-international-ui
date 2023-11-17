from django.urls import re_path

from core.views import QuerystringRedirectView

redirects_for_retired_pages_that_must_come_before_tree_based_routing = [
    # All of these can be used to discover which view code we need to delete
    re_path(
        # Redirect the old invest homepage to atlas
        r'^international/invest[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
    ),
    re_path(
        # Redirect the old capital invest contact form to to atlas
        r'^international/content/capital-invest/contact[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/contact/'
        ),
    ),
    re_path(
        # Redirect the old capital invest homepage to atlas
        r'^international/content/capital-invest[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
    ),
    re_path(
        r'^international/content/capital-invest/how-we-help-you-invest-capital[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/'
        ),
    ),
    re_path(
        # Old CIOs
        r'^international/content/opportunities[/]*',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    re_path(
        # Old HPOs
        r'^international/content/invest/high-potential-opportunities[/]*',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    re_path(
        r'^international/content/about-us[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/'
        ),
    ),

    # How to expand UK setup
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/establish-a-base-for-business-in-the-uk/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/research-and-development-rd-support-in-the-uk/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/global-entrepreneur-program[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/global-entrepreneur-program/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/uk-visas-and-migration[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/uk-visas-and-migration/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/register-a-company-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/register-a-company-in-the-uk/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/hire-skilled-workers-for-your-uk-operations/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/open-a-uk-business-bank-account/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/uk-tax-and-incentives[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/uk-tax-and-incentives/'
        ),
    ),
    re_path(
        r'^international/content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk[/]*',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/access-finance-in-the-uk/'
        ),
    ),

    re_path(
        # Redirect the rest of the 'invest' CMS page and all its tree-based children
        r'^international/content/invest/',
        QuerystringRedirectView.as_view(pattern_name='atlas-home'),
    ),

    # About the UK was moved over to Why Invest in the UK
    re_path(
        r'^international/content/about-uk[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/why-choose-uk[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/why-choose-uk/tax-incentives[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/tax-incentives/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/why-choose-uk/uk-talent-and-labour[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/uk-talent-and-labour/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/why-choose-uk/uk-innovation[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/uk-innovation/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/why-choose-uk/uk-infrastructure[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/why-invest-in-the-uk/uk-infrastructure/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/industries[/]*',  # NB: wildcard
        QuerystringRedirectView.as_view(
            url='/international/content/investment/sectors/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/regions[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/'
        ),
    ),
    re_path(
        r'^international/content/about-uk/regions/scotland[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/scotland/'
        ),
    ),

    re_path(
        r'^international/content/about-uk/regions/northern-ireland[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/northern-ireland/'
        ),
    ),

    re_path(
        r'^international/content/about-uk/regions/north-england[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/north-england/'
        ),
    ),

    re_path(
        r'^international/content/about-uk/regions/wales[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/wales/'
        ),
    ),

    re_path(
        r'^international/content/about-uk/regions/midlands[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/midlands/'
        ),
    ),

    re_path(
        r'^international/content/about-uk/regions/south-england[/]*$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/regions/south-england/'
        ),
    ),
]

redirects_before_tree_based_routing_lookup = [
    # These ones are inserted into the urlconf before the 'cms-page-from-path' route is tried
    # so we can redirect pages that otherwise came from tree-based routing
    re_path(
        r'^international/content/opportunities[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    re_path(
        r'^international/content/investment/opportunities[/]*$',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
    re_path(
        r'^international/content/invest/high-potential-opportunities/contact[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form'
        )
    ),
    re_path(
        r'^international/content/invest/high-potential-opportunities/contact/success[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form-success'
        )
    ),
    re_path(
        r'^international/content/expand/high-potential-opportunities/contact[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form'
        )
    ),
    re_path(
        r'^international/content/expand/high-potential-opportunities/contact/success[/]*$',
        QuerystringRedirectView.as_view(
            pattern_name='fdi-opportunity-request-form-success'
        )
    ),
    re_path(
        r'^vca/$',
        QuerystringRedirectView.as_view(
            url='/international/content/investment/how-we-can-help/the-venture-capital-unit/'
        ),
    ),
] + redirects_for_retired_pages_that_must_come_before_tree_based_routing
