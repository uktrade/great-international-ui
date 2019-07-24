import random

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response

from directory_constants.choices import COUNTRY_CHOICES
from directory_constants import urls
from directory_components.helpers import get_user_country, SocialLinkBuilder
from directory_components.mixins import (
    CMSLanguageSwitcherMixin,
    GA360Mixin, CountryDisplayMixin, InternationalHeaderMixin)

from core import forms, helpers, constants
from core.context_modifiers import (
    register_context_modifier,
    registry as context_modifier_registry
)
from core.templatetags.cms_tags import filter_by_active_language
from core.mixins import NotFoundOnDisabledFeature, RegionalContentMixin


class InternationalView(InternationalHeaderMixin, GA360Mixin, TemplateView):
    pass


class CMSPageFromPathView(
    RegionalContentMixin,
    CMSLanguageSwitcherMixin,
    NotFoundOnDisabledFeature,
    InternationalView
):
    cms_site_id = settings.DIRECTORY_CMS_SITE_ID

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super().dispatch(request, *args, **kwargs)
        page_type = self.page['page_type']
        ga360_data = helpers.get_ga_data_for_page(page_type)
        self.set_ga360_payload(
            page_id=page_type,
            business_unit=ga360_data['business_unit'],
            site_section=ga360_data['site_section'],
            site_subsection=ga360_data['site_subsection']
        )
        return dispatch_result

    @property
    def template_name(self):
        return constants.TEMPLATE_MAPPING[self.page['page_type']]

    @property
    def header_section(self):
        return constants.HEADER_MAPPING[self.page['page_type']]

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=self.cms_site_id,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(page=self.page, **kwargs)

        flag_name = constants.FEATURE_FLAGGED_PAGE_TYPES_MAPPING.get(self.page['page_type'])

        if flag_name and not settings.FEATURE_FLAGS[flag_name]:
            raise Http404

        for modifier in context_modifier_registry.get_for_page_type(
            self.page['page_type']
        ):
            context.update(modifier(context, request=self.request))

        return context


@register_context_modifier('InternationalArticlePage')
def article_page_context_modifier(context, request):

    page_title = context['page'].get('article_title', '')

    social_links_builder = SocialLinkBuilder(
        request.build_absolute_uri(),
        page_title,
        'great.gov.uk')

    return {
        'social_links': social_links_builder.links
    }


@register_context_modifier('InternationalHomePage')
def home_page_context_modifier(context, request):

    country_code = get_user_country(request)
    country_name = dict(COUNTRY_CHOICES).get(country_code, '')

    return {
        'tariffs_country': {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        },
        'tariffs_country_selector_form': forms.TariffsCountryForm(
            initial={'tariffs_country': country_code}
        ),
    }


@register_context_modifier('InternationalTopicLandingPage')
def sector_landing_page_context_modifier(context, request):

    def rename_heading_field(page):
        page['landing_page_title'] = page['heading']
        return page

    context['page']['child_pages'] = [
        rename_heading_field(child_page)
        for child_page in context['page']['child_pages']]

    return context


@register_context_modifier('InternationalSectorPage')
def sector_page_context_modifier(context, request):
    page = context['page']

    trade_contact_form = urls.build_fas_url('industries/contact/')

    if 'related_opportunities' in page:
        random.shuffle(page['related_opportunities'])
        random_opportunities = page['related_opportunities'][0:3]
    else:
        random_opportunities = []

    return {
        'invest_contact_us_url': urls.build_invest_url('contact/'),
        'num_of_statistics': helpers.count_data_with_field(
            page['statistics'], 'number'),
        'section_three_num_of_subsections': helpers.count_data_with_field(
            page['section_three_subsections'], 'heading'),
        'random_opportunities': random_opportunities,
        'trade_contact_form_url': trade_contact_form
        }


@register_context_modifier('AboutUkWhyChooseTheUkPage')
def about_uk_why_choose_the_uk_page_context_modifier(context, request):

    def count_data_with_field(list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    page = context['page']

    return {
        'num_of_statistics': count_data_with_field(
            page['statistics'],
            'number'
        )
    }


@register_context_modifier('InternationalSubSectorPage')
def sub_sector_context_modifier(context, request):
    page = context['page']

    trade_contact_form = urls.build_fas_url('industries/contact/')

    if 'related_opportunities' in page:
        random.shuffle(page['related_opportunities'])
        random_opportunities = page['related_opportunities'][0:3]
    else:
        random_opportunities = []

    return {
        'invest_contact_us_url': urls.build_invest_url('contact/'),
        'num_of_statistics': helpers.count_data_with_field(
            page['statistics'], 'number'),
        'section_three_num_of_subsections': helpers.count_data_with_field(
            page['section_three_subsections'], 'heading'),
        'random_opportunities': random_opportunities,
        'trade_contact_form_url': trade_contact_form
        }


class InternationalContactPageView(CountryDisplayMixin, InternationalView):
    template_name = 'core/contact_page.html'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InternationalContactPage',
            business_unit='GreatInternational',
            site_section='Contact',
            site_subsection='ContactForm'
        )

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            hide_language_selector=True,
            invest_contact_us_url=urls.build_invest_url('contact/'),
            *args, **kwargs
        )


@register_context_modifier('CapitalInvestRegionPage')
def capital_invest_region_page_context_modifier(context, request):
    page = context['page']

    show_accordions = False

    if 'subsections' in page:
        accordions = {accordion['title']: accordion['content']
                      for accordion in page['subsections']
                      if accordion['title'] and accordion['content']}
        if accordions:
            show_accordions = True

    return {
        'num_of_economics_statistics': helpers.count_data_with_field(
            page['economics_stats'], 'number'),
        'num_of_location_statistics': helpers.count_data_with_field(
            page['location_stats'], 'number'),
        'invest_cta_link': urls.SERVICES_INVEST,
        'buy_cta_link': urls.SERVICES_FAS,
        'show_accordions': show_accordions
    }


@register_context_modifier('CapitalInvestOpportunityPage')
def capital_invest_opportunity_page_context_modifier(context, request):

    page = context['page']
    random_sector = ''
    opps_in_random_sector = []

    if 'related_sectors' in page and page['related_sectors']:
        sectors = [sector['related_sector']['heading']
                   for sector in page['related_sectors']
                   if sector['related_sector']]
        random.shuffle(sectors)
        random_sector = sectors[0]

    if 'related_sector_with_opportunities' in page \
            and page['related_sector_with_opportunities']:
        opps_in_random_sector = \
            page['related_sector_with_opportunities'][random_sector]
        random.shuffle(opps_in_random_sector)

    return {
        'invest_cta_link': urls.SERVICES_INVEST,
        'buy_cta_link': urls.SERVICES_FAS,
        'random_related_sector_title': random_sector,
        'random_opps_in_random_related_sector': opps_in_random_sector[0:3]
    }


class OpportunitySearchView(
    CountryDisplayMixin,
    InternationalView
):
    template_name = 'core/capital_invest/capital_invest_opportunity_listing_page.html'  # NOQA
    page_size = 10
    header_section = 'invest'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='GreatInternationalCapitalInvestmentOpportunitySearch',
            business_unit='CapitalInvestment',
            site_section='Opportunities',
            site_subsection='Search'
        )

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except (EmptyPage, PageNotAnInteger):
            url = helpers.get_paginator_url(self.request.GET, 'opportunities') + "&page=1"  # NOQA
            return redirect(url)

    @property
    def page_number(self):
        return self.request.GET.get('page', '1')

    @property
    def sector(self):
        return helpers.SectorFilter(self.request.GET.getlist('sector', []))

    @property
    def scale(self):
        return helpers.ScaleFilter(self.request.GET.getlist('scale', []))

    @property
    def region(self):
        return helpers.RegionFilter(self.request.GET.getlist('region', ''))

    @property
    def sort_filter(self):
        return helpers.SortFilter(self.request.GET.get('sort_by', ''))

    @property
    def sub_sector(self):
        return helpers.SubSectorFilter(self.request.GET.getlist('sub_sector', []))

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=settings.DIRECTORY_CMS_SITE_ID,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    @property
    def opportunities(self):
        if 'opportunity_list' in self.page:
            return self.page['opportunity_list']
        else:
            return []

    @property
    def all_sectors(self):
        sectors = set()

        for opp in self.opportunities:
            for sector in opp['related_sectors']:
                if sector['related_sector'] \
                        and sector['related_sector']['heading']:
                    sectors.add(sector['related_sector']['heading'])
        sectors = list(sectors)
        sectors.sort()
        return [
            (sector, sector) for sector in sectors
        ]

    @property
    def all_scales(self):
        return [
            (scale.title, scale.title)
            for scale in helpers.ScaleFilter.scales_with_values
        ]

    @property
    def all_regions(self):
        regions = set()
        for opp in self.opportunities:
            if opp['related_region'] and opp['related_region']['title']:
                regions.add(opp['related_region']['title'])
        regions = list(regions)
        regions.sort()
        return [
            (region, region) for region in regions
        ]

    @property
    def all_sort_filters(self):
        sort_filters_with_selected_status = [
            (sort_filter.title, sort_filter.title)
            for sort_filter in helpers.SortFilter.sort_by_with_values
        ]

        return sort_filters_with_selected_status

    @property
    def all_sub_sectors_for_sectors_chosen(self):

        if self.sector.sectors and 'sector_with_sub_sectors' in self.page:
            sub_sectors_from_sector_chosen = {
                sub for sector in self.sector.sectors
                for sub in self.page['sector_with_sub_sectors'][sector]
            }
            sub_sectors_from_selected = set(self.sub_sector.sub_sectors)

            all_sub_sectors = sub_sectors_from_sector_chosen.union(
                sub_sectors_from_selected)
        else:
            all_sub_sectors = {sub_sector for opp in self.opportunities
                               for sub_sector in opp['sub_sectors'] or []}

        all_sub_sectors = list(all_sub_sectors)
        all_sub_sectors.sort()

        return [
            (sub_sector, sub_sector) for sub_sector in all_sub_sectors
        ]

    @property
    def filtered_opportunities(self):

        filtered_opportunities = [opp for opp in self.opportunities]

        if self.sector.sectors:
            filtered_opportunities = helpers.filter_opportunities(
                filtered_opportunities,
                self.sector
            )

        if self.region.regions:
            filtered_opportunities = helpers.filter_opportunities(
                filtered_opportunities,
                self.region
            )

        if self.scale.selected_scales:
            filtered_opportunities = helpers.filter_opportunities(
                filtered_opportunities,
                self.scale
            )

        if self.sub_sector.sub_sectors:
            filtered_opportunities = helpers.filter_opportunities(
                filtered_opportunities,
                self.sub_sector
            )

        if self.sort_filter.sort_by_filter_chosen:
            filtered_opportunities = helpers.sort_opportunities(
                filtered_opportunities,
                self.sort_filter
            )

        return filtered_opportunities

    @property
    def num_of_opportunities(self):
        return len(self.filtered_opportunities)

    @property
    def pagination(self):
        paginator = Paginator(self.filtered_opportunities, self.page_size)
        return paginator.page(self.page_number or 1)

    @property
    def filters_chosen(self):
        filters = []
        for sector in self.sector.sectors:
            filters.append(sector)
        for scale in self.scale.selected_scales:
            filters.append(scale.title)
        for region in self.region.regions:
            filters.append(region)
        for sub_sector in self.sub_sector.sub_sectors:
            filters.append(sub_sector)
        return filters

    @property
    def sorting_chosen(self):
        return self.sort_filter.sort_by_filter_chosen.title

    @property
    def opportunity_search_form(self):
        return forms.OpportunitySearchForm(
            sectors=self.all_sectors,
            scales=self.all_scales,
            regions=self.all_regions,
            sort_by_options=self.all_sort_filters,
            sub_sectors=self.all_sub_sectors_for_sectors_chosen,
            initial={
                'sector': self.filters_chosen,
                'scale': self.filters_chosen,
                'region': self.filters_chosen,
                'sort_by': self.sorting_chosen,
                'sub_sector': self.filters_chosen
            },
        )

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            invest_url=urls.SERVICES_INVEST,
            num_of_opportunities=self.num_of_opportunities,
            sectors=self.all_sectors,
            scales=self.all_scales,
            regions=self.all_regions,
            sorting_filters=self.all_sort_filters,
            sub_sectors=self.all_sub_sectors_for_sectors_chosen,
            pagination=self.pagination,
            sorting_chosen=self.sorting_chosen,
            filters=self.filters_chosen,
            current_page_num=self.page_number,
            form=self.opportunity_search_form,
            *args, **kwargs,
        )


@register_context_modifier('InvestInternationalHomePage')
def invest_homepage_context_modifier(context, request):
    pages = context['page']['high_potential_opportunities'],

    return {
        'international_home_page_link': urls.GREAT_INTERNATIONAL,
        'investment_support_directory_link': urls.FAS_INVESTMENT_SUPPORT_DIRECTORY,
        'how_to_set_up_visas_and_migration_link': urls.GREAT_INTERNATIONAL_HOW_TO_SET_UP_VISAS_AND_MIGRATION,
        'how_to_set_up_tax_and_incentives_link': urls.GREAT_INTERNATIONAL_HOW_TO_SET_UP_TAX_AND_INCENTIVES,
        'show_hpo_section': bool(
            pages and filter_by_active_language(pages[0])
        ),
    }
