from django.utils import translation
import requests


def create_response(status_code=200, json_payload=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_payload or {}
    return response


def unslugify(slug):
    return slug.replace('-', ' ').capitalize()


def get_language_from_querystring(request):
    language_codes = translation.trans_real.get_languages()
    language_code = request.GET.get('language') or request.GET.get('lang')
    if language_code and language_code in language_codes:
        return language_code


GA_DATA_MAPPING = {
    'InternationalHomePage': {
        'business_unit': 'International',
        'site_section': 'HomePage',
        'site_subsection': ''
    },
    'InternationalTopicLandingPage': {
        'business_unit': 'International',
        'site_section': 'Topic',
        'site_subsection': 'ListingPage'
    },
    'InternationalArticleListingPage': {
        'business_unit': 'International',
        'site_section': 'Article',
        'site_subsection': 'ListingPage'
    },
    'InternationalArticlePage': {
        'business_unit': 'International',
        'site_section': 'Article',
        'site_subsection': 'DetailPage'
    },
    'InternationalCampaignPage': {
        'business_unit': 'International',
        'site_section': 'Campaign',
        'site_subsection': 'LandingPage'
    },
    'InternationalSectorPage': {
        'business_unit': 'International',
        'site_section': 'Sector',
        'site_subsection': 'DetailPage'
    },
    'InternationalCuratedTopicLandingPage': {
        'business_unit': 'International',
        'site_section': 'CuratedTopic',
        'site_subsection': 'LandingPage'
    },
    'InternationalGuideLandingPage': {
        'business_unit': 'Invest',
        'site_section': 'Guide',
        'site_subsection': 'ListingPage'
    },
    'InternationalEUExitFormPage': {
        'business_unit': 'International',
        'site_section': 'EUExit',
        'site_subsection': 'FormPage'
    },
    'InternationalEUExitFormSuccessPage': {
        'business_unit': 'International',
        'site_section': 'EUExit',
        'site_subsection': 'FormSuccessPage'
    },
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
    'CapitalInvestRegionalSectorPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Region',
        'site_subsection': 'SectorPage'
    },
    'CapitalInvestOpportunityPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Opportunity',
        'site_subsection': 'DetailPage'
    },
}


def get_ga_data_for_page(page_type):
    return GA_DATA_MAPPING[page_type]
