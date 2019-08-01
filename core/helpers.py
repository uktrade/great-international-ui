from collections import namedtuple
from urllib.parse import urlencode
from django.urls import reverse
import collections

import directory_components.helpers
from directory_api_client.client import api_client
from django.http import Http404
from django.utils import translation
import requests

from directory_constants import choices
from django.utils.html import escape, mark_safe
from core import constants


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


NotifySettings = collections.namedtuple(
    'NotifySettings',
    [
        'company_template',
        'support_template',
        'investor_template',
        'support_email_address',
    ]
)


def get_ga_data_for_page(page_type):
    return constants.GA_DATA_MAPPING[page_type]


def get_header_section(page_type):
    return constants.HEADER_MAPPING[page_type][0]


def get_header_subsection(page_type):
    return constants.HEADER_MAPPING[page_type][1]


def get_paginator_url(filters, url_name):
    url = reverse(url_name)

    querystring = urlencode({
        key: value
        for key, value in filters.lists()
        if value and key != 'page'
    }, doseq=True)
    return f'{url}?{querystring}'


class SectorFilter:
    def __init__(self, sectors):
        self.sectors = sectors

    def matches(self, opportunity):
        return any(
            sector['related_sector'].get('heading') in self.sectors
            for sector in opportunity.get('related_sectors', [])
            if sector['related_sector'] and sector['related_sector']['heading']
        )


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
                elif float(opportunity['scale_value']) == 0.00:
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


class SubSectorFilter:
    def __init__(self, sub_sectors):
        self.sub_sectors = sub_sectors

    def matches(self, opportunity):
        if 'sub_sectors' in opportunity and opportunity['sub_sectors']:
            for sub_sector in opportunity['sub_sectors']:
                if sub_sector in self.sub_sectors:
                    return True
        return False


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
            (sort_by for sort_by
             in self.sort_by_with_values
             if sort_by.title == sort_by_filter_chosen),
            self.sort_by_with_values[0])


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


class CompanyParser(directory_components.helpers.CompanyParser):

    def serialize_for_template(self):
        if not self.data:
            return {}
        return {
            **self.data,
            'date_of_creation': self.date_of_creation,
            'address': self.address,
            'sectors': self.sectors_label,
            'keywords': self.keywords,
            'employees': self.employees_label,
            'expertise_industries': self.expertise_industries_label,
            'expertise_regions': self.expertise_regions_label,
            'expertise_countries': self.expertise_countries_label,
            'expertise_languages': self.expertise_languages_label,
            'has_expertise': self.has_expertise,
            'expertise_products_services': (
                self.expertise_products_services_label
            ),
            'is_in_companies_house': self.is_in_companies_house,
        }


def get_results_from_search_response(response):
    parsed = response.json()
    formatted_results = []

    for result in parsed['hits']['hits']:
        parser = CompanyParser(result['_source'])
        formatted = parser.serialize_for_template()
        if 'highlight' in result:
            highlighted = '...'.join(
                result['highlight'].get('description', '') or
                result['highlight'].get('summary', '')
            )
            # escape all html tags other than <em> and </em>
            highlighted_escaped = (
                escape(highlighted)
                .replace('&lt;em&gt;', '<em>')
                .replace('&lt;/em&gt;', '</em>')
            )
            formatted['highlight'] = mark_safe(highlighted_escaped)
        formatted_results.append(formatted)

    parsed['results'] = formatted_results
    return parsed


def get_filters_labels(filters):
    sectors = dict(choices.INDUSTRIES)
    languages = dict(choices.EXPERTISE_LANGUAGES)
    labels = []
    skip_fields = [
        'q',
        'page',
        # Prevents duplicates labels not to be displayed in filter list
        'expertise_products_services_label'
    ]
    for name, values in filters.items():
        if name in skip_fields:
            pass
        elif name == 'industries':
            labels += [sectors[item] for item in values if item in sectors]
        elif name == 'expertise_languages':
            labels += [languages[item] for item in values if item in languages]
        elif name.startswith('expertise_products_services_'):
            labels += values
        else:
            for value in values:
                labels.append(value.replace('_', ' ').title())
    return labels


def get_company_profile(number):
    response = api_client.company.retrieve_public_profile(number=number)
    if response.status_code == 404:
        raise Http404(f'API returned 404 for company number {number}')
    response.raise_for_status()
    return response.json()


def count_data_with_field(list_of_data, field):
    filtered_list = [item for item in list_of_data if item[field]]
    return len(filtered_list)
