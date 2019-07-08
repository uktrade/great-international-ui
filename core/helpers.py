from collections import namedtuple
from urllib.parse import urlencode
from django.urls import reverse
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
}


def get_ga_data_for_page(page_type):
    return GA_DATA_MAPPING[page_type]


def get_paginator_url(filters, url_name):
    url = reverse(url_name)

    querystring = urlencode({
        key: value
        for key, value in filters.items()
        if value and key != 'page'
    }, doseq=True)
    return f'{url}?{querystring}'


class SectorFilter:
    def __init__(self, sectors):
        self.sectors = sectors

    def matches(self, opportunity):
        if opportunity['related_sectors']:
            for sector in opportunity['related_sectors']:
                if sector['related_sector'] \
                        and sector['related_sector']['title'] \
                        and sector['related_sector']['title'] in self.sectors:
                    return True


Scale = namedtuple("Scale", "title min max")


class ScaleFilter:
    scales_with_values = [
        Scale(title='< £100m', min=1, max=99),
        Scale(title='£100m - £499m', min=100, max=499),
        Scale(title='£500m - £999m', min=500, max=999),
        Scale(title='> £1bn', min=1000, max='None'),
        Scale(title='Value unknown', min=0, max=0)
    ]

    def __init__(self, scale_strings):
        self.selected_scales = [
            scaleFilter for scaleFilter in self.scales_with_values
            if scaleFilter.title in scale_strings
        ]

    def matches(self, opportunity):
        for scale_chosen in self.selected_scales:
            if scale_chosen.min == 0 and scale_chosen.max == 0:
                if not opportunity['scale_value']:
                    return True
            elif scale_chosen.max == 'None':
                if scale_chosen.min <= float(opportunity['scale_value']):
                    return True
            elif scale_chosen.max:
                if scale_chosen.min <= float(opportunity['scale_value']) <= scale_chosen.max:  # NOQA
                    return True


class RegionFilter:
    def __init__(self, regions):
        self.regions = regions

    def matches(self, opportunity):
        if opportunity['related_region'] \
                and opportunity['related_region']['title'] \
                and opportunity['related_region']['title'] in self.regions:
            return True


def filter_opportunities(opportunities, filter_chosen):
    return [opp for opp in opportunities if filter_chosen.matches(opp)]


Sort_by = namedtuple("Sort_by", "title value reverse")


class SortFilter:
    sort_by_with_values = [
        Sort_by(title='Project name: A to Z', value='title', reverse=False),
        Sort_by(title='Project name: Z to A', value='title', reverse=True),
        Sort_by(
            title='Scale: Low to High', value='scale_value', reverse=False
        ),
        Sort_by(title='Scale: High to Low', value='scale_value', reverse=True)
    ]

    def __init__(self, sort_by_filter_chosen):
        self.sort_by_filter_chosen = next(
            (sort_by for sort_by in self.sort_by_with_values
             if sort_by.title == sort_by_filter_chosen), '')


def sort_opportunities(opportunities, sort_by_chosen):
    sort_filter = sort_by_chosen.sort_by_filter_chosen
    if sort_filter.value == 'title':
        opportunities.sort(
            key=lambda x: x['title'],
            reverse=sort_filter.reverse
        )

    if sort_filter.value == 'scale_value':
        opportunities.sort(
            key=lambda x: float(x['scale_value']),
            reverse=sort_filter.reverse
        )

    return opportunities
