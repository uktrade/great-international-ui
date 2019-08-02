
TEMPLATE_MAPPING = {
    # Great international core
    'InternationalHomePage': 'core/landing_page.html',
    'InternationalTopicLandingPage': 'core/topic_list.html',
    'InternationalArticleListingPage': 'core/article_list.html',
    'InternationalArticlePage': 'core/uk_setup_guide/article_detail.html',
    'InternationalCampaignPage': 'core/campaign.html',
    'InternationalSectorPage': 'core/sector_page.html',
    'InternationalSubSectorPage': 'core/sector_page.html',
    'InternationalCuratedTopicLandingPage':
        'core/how_to_do_business_landing_page.html',
    'InternationalGuideLandingPage':
        'core/uk_setup_guide/guide_landing_page.html',

    # Brexit
    'InternationalEUExitFormPage': 'euexit/international-contact-form.html',
    'InternationalEUExitFormSuccessPage':
        'euexit/international-contact-form-success.html',

    # Capital investment
    'InternationalCapitalInvestLandingPage':
        'core/capital_invest/capital_invest_landing_page.html',
    'CapitalInvestRegionPage':
        'core/capital_invest/capital_invest_region_page.html',
    'CapitalInvestOpportunityPage':
        'core/capital_invest/capital_invest_opportunity_page.html',
    'CapitalInvestOpportunityListingPage':
        'core/capital_invest/capital_invest_opportunity_listing_page.html',

    # About DIT
    'AboutDitLandingPage': 'core/about_dit/about_dit_landing_page.html',
    'AboutDitServicesPage': 'core/about_dit/services_page.html',
    'AboutUkWhyChooseTheUkPage': 'core/about_uk/why_choose_the_uk_page.html',

    # Invest
    'InvestInternationalHomePage': 'invest/landing_page.html',
    'InvestHighPotentialOpportunityDetailPage':
        'invest/hpo/high_potential_opportunity_detail.html',
    'InvestHighPotentialOpportunityFormPage': 'invest/hpo/high_potential_opportunities_form.html',
    'InvestHighPotentialOpportunityFormSuccessPage':
        'invest/hpo/high_potential_opportunities_form_success.html',
    'InvestRegionPage': 'invest/regions/region_detail.html',

    # Find a supplier
    'InternationalTradeHomePage': 'find_a_supplier/landing_page.html',
}

FEATURE_FLAGGED_URLS_MAPPING = {
    '/international/content/how-to-do-business-with-the-uk/':
        'HOW_TO_DO_BUSINESS_ON',
}

FEATURE_FLAGGED_PAGE_TYPES_MAPPING = {
    'CapitalInvestRegionPage':
        'CAPITAL_INVEST_REGION_PAGE_ON',
    'CapitalInvestOpportunityPage':
        'CAPITAL_INVEST_OPPORTUNITY_PAGE_ON',
    'InternationalCapitalInvestLandingPage':
        'CAPITAL_INVEST_LANDING_PAGE_ON',
    'CapitalInvestOpportunityListingPage':
        'CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ON',
    'InternationalSubSectorPage':
        'CAPITAL_INVEST_SUB_SECTOR_PAGE_ON'
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
    'InternationalCampaignPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Campaign',
        'site_subsection': 'LandingPage'
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
    'AboutUkWhyChooseTheUkPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'WhyChooseTheUkPage'
    },

    # Find a supplier
    'InternationalTradeHomePage': {
        'business_unit': 'FindASupplier',
        'site_section': 'LandingPage',
        'site_subsection': ''
    },
}

HEADER_MAPPING = {
    # Great international core
    'InternationalHomePage': '',
    'InternationalTopicLandingPage': 'industries',
    'InternationalArticleListingPage': 'uk_setup_guide',
    'InternationalArticlePage': 'uk_setup_guide',
    'InternationalCampaignPage': '',
    'InternationalSectorPage': 'industries',
    'InternationalSubSectorPage': 'industries',
    'InternationalCuratedTopicLandingPage': 'uk_setup_guide',
    'InternationalGuideLandingPage': 'uk_setup_guide',

    # Brexit
    'InternationalEUExitFormPage': '',
    'InternationalEUExitFormSuccessPage': '',

    # Capital investment
    'InternationalCapitalInvestLandingPage': 'invest',
    'CapitalInvestRegionPage': 'invest',
    'CapitalInvestOpportunityPage': 'invest',
    'CapitalInvestOpportunityListingPage': 'invest',

    # Invest
    'InvestInternationalHomePage': 'invest',
    'InvestHighPotentialOpportunityDetailPage': 'invest',
    'InvestHighPotentialOpportunityFormPage': 'invest',
    'InvestHighPotentialOpportunityFormSuccessPage': 'invest',

    # About DIT
    'AboutDitLandingPage': '',
    'AboutDitServicesPage': '',
    'AboutUkWhyChooseTheUkPage': '',
}
