from collections import namedtuple
from core.header_config import tier_one_nav_items as tier_one, tier_two_nav_items as tier_two


TEMPLATE_MAPPING = {
    # Great international core
    'InternationalHomePage': 'core/landing_page.html',
    'InternationalTopicLandingPage': 'core/topic_list.html',
    'InternationalArticleListingPage': 'core/article_list.html',
    'InternationalArticlePage': 'core/article_detail.html',
    'InternationalSectorPage': 'core/sector_page.html',
    'InternationalSubSectorPage': 'core/sector_page.html',
    'InternationalCuratedTopicLandingPage': 'core/how_to_do_business_landing_page.html',
    'InternationalGuideLandingPage': 'core/uk_setup_guide/guide_landing_page.html',

    # Brexit
    'InternationalEUExitFormPage': 'euexit/international-contact-form.html',
    'InternationalEUExitFormSuccessPage': 'euexit/international-contact-form-success.html',

    # Capital investment
    'InternationalCapitalInvestLandingPage': 'core/capital_invest/capital_invest_landing_page.html',
    'CapitalInvestRegionPage': 'core/capital_invest/capital_invest_region_page.html',
    'CapitalInvestOpportunityPage': 'core/capital_invest/capital_invest_opportunity_page.html',
    'CapitalInvestOpportunityListingPage': 'core/capital_invest/capital_invest_opportunity_listing_page.html',
    'CapitalInvestContactFormPage': 'core/capital_invest/capital_invest_contact_form.html',
    'CapitalInvestContactFormSuccessPage': 'core/capital_invest/capital_invest_contact_form_success.html',

    # About DIT
    'AboutDitLandingPage': 'core/about_dit/about_dit_landing_page.html',
    'AboutDitServicesPage': 'core/about_dit/services_page.html',
    'AboutUkLandingPage': 'core/about_uk/about_uk_landing_page.html',
    'AboutUkRegionListingPage': 'core/about_uk/about_uk_region_listing_page.html',
    'AboutUkRegionPage': 'core/about_uk/about_uk_region_page.html',
    'AboutUkWhyChooseTheUkPage': 'core/about_uk/why_choose_the_uk_page.html',

    # Invest
    'InvestInternationalHomePage': 'invest/landing_page.html',
    'InvestHighPotentialOpportunityDetailPage': 'invest/hpo/high_potential_opportunity_detail.html',
    'InvestHighPotentialOpportunityFormPage': 'invest/hpo/high_potential_opportunities_form.html',
    'InvestHighPotentialOpportunityFormSuccessPage': 'invest/hpo/high_potential_opportunities_form_success.html',
    'InvestRegionPage': 'invest/regions/region_detail.html',

    # Find a supplier
    'InternationalTradeHomePage': 'find_a_supplier/landing_page.html',
    'InternationalTradeIndustryContactPage': 'find_a_supplier/industry-contact.html',

    # Ready to Trade
    'ReadyToTradeLandingPage': 'core/ready_to_trade_landing_page.html'
}

FEATURE_FLAGGED_URLS_MAPPING = {
    '/international/content/how-to-do-business-with-the-uk/':
        'HOW_TO_DO_BUSINESS_ON',
}

FEATURE_FLAGGED_PAGE_TYPES_MAPPING = {
    'CapitalInvestRegionPage':
        'CAPITAL_INVEST_REGION_PAGE_ON',
    'AboutUkRegionPage':
        'ABOUT_UK_REGION_PAGE_ON',
    'AboutUkRegionListingPage':
        'ABOUT_UK_REGION_LISTING_PAGE_ON',
    'CapitalInvestOpportunityPage':
        'CAPITAL_INVEST_OPPORTUNITY_PAGE_ON',
    'InternationalCapitalInvestLandingPage':
        'CAPITAL_INVEST_LANDING_PAGE_ON',
    'CapitalInvestOpportunityListingPage':
        'CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ON',
    'InternationalSubSectorPage':
        'CAPITAL_INVEST_SUB_SECTOR_PAGE_ON',
    'CapitalInvestContactFormPage':
        'CAPITAL_INVEST_CONTACT_FORM_PAGE_ON',
    'CapitalInvestContactFormSuccessPage':
        'CAPITAL_INVEST_CONTACT_FORM_PAGE_ON',
    'InternationalTradeIndustryContactPage':
        'FIND_A_SUPPLIER_ON',
}

GA_DATA_MAPPING = {
    # Great international core
    'InternationalHomePage': {
        'business_unit': 'GreatInternational',
        'site_section': 'HomePage',
        'site_subsection': ''
    },
    'InternationalTopicLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Topic',
        'site_subsection': 'ListingPage'
    },
    'InternationalArticleListingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Article',
        'site_subsection': 'ListingPage'
    },
    'InternationalArticlePage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Article',
        'site_subsection': 'DetailPage'
    },
    'InternationalSectorPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Sector',
        'site_subsection': 'DetailPage'
    },
    'InternationalSubSectorPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'SubSector',
        'site_subsection': 'DetailPage'
    },
    'InternationalCuratedTopicLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'CuratedTopic',
        'site_subsection': 'LandingPage'
    },
    'InternationalGuideLandingPage': {
        'business_unit': 'Invest',
        'site_section': 'Guide',
        'site_subsection': 'ListingPage'
    },

    # Brexit
    'InternationalEUExitFormPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'EUExit',
        'site_subsection': 'FormPage'
    },
    'InternationalEUExitFormSuccessPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'EUExit',
        'site_subsection': 'FormSuccessPage'
    },

    # Capital investment
    'InternationalCapitalInvestLandingPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'LandingPage',
        'site_subsection': ''
    },
    'CapitalInvestRegionPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Region',
        'site_subsection': 'DetailPage'
    },
    'CapitalInvestOpportunityPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Opportunity',
        'site_subsection': 'DetailPage'
    },
    'CapitalInvestOpportunityListingPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Opportunity',
        'site_subsection': 'ListingPage'
    },
    'CapitalInvestContactFormPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'CapitalInvest',
        'site_subsection': 'Contact',
    },
    'CapitalInvestContactFormSuccessPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'CapitalInvest',
        'site_subsection': 'ContactSuccess'
    },

    # Invest
    'InvestInternationalHomePage': {
        'business_unit': 'Invest',
        'site_section': 'HomePage',
        'site_subsection': ''
    },
    'InvestHighPotentialOpportunityDetailPage': {
        'business_unit': 'Invest',
        'site_section': 'HighPotentialOpportunities',
        'site_subsection': 'DetailPage',
    },
    'InvestHighPotentialOpportunityFormPage': {
        'business_unit': 'Invest',
        'site_section': 'HighPotentialOpportunities',
        'site_subsection': 'FormPage',
    },
    'InvestHighPotentialOpportunityFormSuccessPage': {
        'business_unit': 'Invest',
        'site_section': 'HighPotentialOpportunities',
        'site_subsection': 'FormSuccessPage',
    },
    'InvestRegionPage': {
        'business_unit': 'Invest',
        'site_section': 'Regions',
        'site_subsection': 'DetailPage',
    },

    # Perfect fit
    'PerfectFitFormPage': {
        'business_unit': 'Invest',
        'site_section': 'PerfectFit',
        'site_subsection': 'FormPage',
    },
    'PerfectFitFormSuccessPage': {
        'business_unit': 'Invest',
        'site_section': 'PerfectFit',
        'site_subsection': 'FormSuccessPage',
    },

    # About DIT
    'AboutDitLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutDIT',
        'site_subsection': 'LandingPage'
    },
    'AboutDitServicesPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutDIT',
        'site_subsection': 'ServicesPage'
    },
    'AboutUkLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'LandingPage'
    },
    'AboutUkRegionListingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'RegionListingPage'
    },
    'AboutUkRegionPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'RegionPage'
    },
    'AboutUkWhyChooseTheUkPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'WhyChooseTheUkPage'
    },

    # Find a supplier
    'InternationalTradeHomePage': {
        'business_unit': 'FindASupplier',
        'site_section': 'HomePage',
        'site_subsection': '',
    },
    'InternationalTradeIndustryContactPage': {
        'business_unit': 'FindASupplier',
        'site_section': 'Industries',
        'site_subsection': 'LandingPageContact'
    },

    # Ready to trade
    'ReadyToTradeLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'ReadyToTradeCampaign',
        'site_subsection': 'ReadyToTrade'
    },
}

HeaderConfig = namedtuple('HeaderConfig', 'section sub_section')
HEADER_SECTION_MAPPING = {
    # Home page
    r'^$': HeaderConfig(section=None, sub_section=None),

    # About the UK pages
    r'^about-uk/why-choose-uk.*': HeaderConfig(section=tier_one.ABOUT_UK, sub_section=tier_two.WHY_CHOOSE_THE_UK),  # noqa
    r'^industries.*': HeaderConfig(section=tier_one.ABOUT_UK, sub_section=tier_two.INDUSTRIES),
    r'^about-uk/industries.*': HeaderConfig(section=tier_one.ABOUT_UK, sub_section=tier_two.INDUSTRIES),
    r'^about-uk/regions.*': HeaderConfig(section=tier_one.ABOUT_UK, sub_section=tier_two.REGIONS),
    r'^about-uk$': HeaderConfig(section=tier_one.ABOUT_UK, sub_section=tier_two.OVERVIEW_ABOUT),
    r'^about-uk.*': HeaderConfig(section=tier_one.ABOUT_UK, sub_section=None),

    # Expand to the UK
    r'^how-to-setup-in-the-uk.*': HeaderConfig(section=tier_one.EXPAND, sub_section=tier_two.HOW_TO_EXPAND),
    r'^(expand|invest)/how-to-setup-in-the-uk.*': HeaderConfig(section=tier_one.EXPAND, sub_section=tier_two.HOW_TO_EXPAND),  # noqa
    r'^(expand|invest)/contact.*': HeaderConfig(section=tier_one.EXPAND, sub_section=tier_two.CONTACT_US_EXPAND),
    r'^(expand|invest)$': HeaderConfig(section=tier_one.EXPAND, sub_section=tier_two.OVERVIEW_EXPAND),
    r'^(expand|invest).*': HeaderConfig(section=tier_one.EXPAND, sub_section=None),

    # Invest Capital in the UK
    r'^opportunities.*': HeaderConfig(section=tier_one.INVEST_CAPITAL, sub_section=tier_two.INVESTMENT_OPPORTUNITIES),  # noqa
    r'^capital-invest/contact.*': HeaderConfig(section=tier_one.INVEST_CAPITAL, sub_section=tier_two.CONTACT_US_INVEST_CAPITAL),  # noqa
    r'^capital-invest$': HeaderConfig(section=tier_one.INVEST_CAPITAL, sub_section=tier_two.OVERVIEW_INVEST_CAPITAL),
    r'^capital-invest.*': HeaderConfig(section=tier_one.INVEST_CAPITAL, sub_section=None),

    # Buy from the UK
    r'^trade/contact.*': HeaderConfig(section=tier_one.TRADE, sub_section=tier_two.CONTACT_US_TRADE),
    r'^trade.*': HeaderConfig(section=tier_one.TRADE, sub_section=tier_two.FIND_A_SUPPLIER),

    # About DIT
    r'^contact.*': HeaderConfig(section=tier_one.ABOUT_DIT, sub_section=tier_two.CONTACT_US_ABOUT_DIT),
    r'^about-dit/contact.*': HeaderConfig(section=tier_one.ABOUT_DIT, sub_section=tier_two.CONTACT_US_ABOUT_DIT),
    r'^about-dit$': HeaderConfig(section=tier_one.ABOUT_DIT, sub_section=tier_two.OVERVIEW_ABOUT_DIT),
    r'^about-dit.*': HeaderConfig(section=tier_one.ABOUT_DIT, sub_section=None),
}
