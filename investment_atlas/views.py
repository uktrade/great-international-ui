from django.shortcuts import redirect

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.functional import cached_property

from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response
from directory_components.mixins import CountryDisplayMixin

from core import helpers as core_helpers
from core.header_config import tier_one_nav_items, tier_two_nav_items
from core.views import InternationalView

from investment_atlas import forms


class InvestmentOpportunitySearchView(CountryDisplayMixin, InternationalView):
    template_name = 'investment_atlas/opportunity_listing_page.html'
    page_size = 10
    header_section = tier_one_nav_items.INVEST_IN_UK
    header_sub_section = tier_two_nav_items.INVESTMENT_OPPORTUNITIES

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='GreatInternationalInvestmentAtlasOpportunitySearch',
            business_unit='InvestmentAtlas',
            site_section='Opportunities',
            site_subsection='Search'
        )

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except (EmptyPage, PageNotAnInteger):
            url = core_helpers.get_paginator_url(self.request.GET, 'atlas-opportunities') + "&page=1"
            return redirect(url)

    @property
    def page_number(self):
        return self.request.GET.get('page', '1')

    @property
    def sector(self):
        return core_helpers.SectorFilter(self.request.GET.getlist('sector', []))

    @property
    def scale(self):
        return core_helpers.ScaleFilter(self.request.GET.getlist('scale', []))

    @property
    def investment_type(self):
        return core_helpers.InvestmentTypeFilter(self.request.GET.getlist('investment_type', []))

    @property
    def planning_status(self):
        return core_helpers.PlanningStatusFilter(self.request.GET.getlist('planning_status', []))

    @property
    def region(self):
        return core_helpers.MultipleRegionsFilter(self.request.GET.getlist('region', ''))

    @property
    def sort_filter(self):
        return core_helpers.SortFilter(self.request.GET.get('sort_by', ''))

    @property
    def sub_sector(self):
        return core_helpers.SubSectorFilter(self.request.GET.getlist('sub_sector', []))

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
                if sector['related_sector'] and sector['related_sector']['heading']:
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
            for scale in core_helpers.ScaleFilter.scales_with_values
        ]

    def all_investment_types(self):
        investment_types = set(
            [opp['investment_type'] for opp in self.opportunities if opp.get('investment_type')]
        )
        investment_types = sorted(list(investment_types))
        return [
            (investment_type, investment_type) for investment_type in investment_types
        ]

    def all_planning_statuses(self):
        planning_statuses = set(
            [opp['planning_status'] for opp in self.opportunities if opp.get('planning_status')]
        )
        planning_statuses = sorted(list(planning_statuses))
        return [
            (planning_status, planning_status) for planning_status in planning_statuses
        ]

    @property
    def all_regions(self):
        regions = set()
        for opp in self.opportunities:
            for related_region in opp.get('related_regions', []):
                if related_region and related_region['title']:
                    regions.add(related_region['title'])
        regions = list(regions)
        regions.sort()
        return [
            (region, region) for region in regions
        ]

    @property
    def all_sort_filters(self):
        sort_filters_with_selected_status = [
            (sort_filter.title, sort_filter.title)
            for sort_filter in core_helpers.SortFilter.sort_by_with_values
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
                               for sub_sector in opp['sub_sectors'] if any(opp['sub_sectors'])}

        all_sub_sectors = list(all_sub_sectors)
        all_sub_sectors.sort()

        return [
            (sub_sector, sub_sector) for sub_sector in all_sub_sectors
        ]

    @property
    def filtered_opportunities(self):

        filtered_opportunities = [opp for opp in self.opportunities]

        if self.sector.sectors:
            filtered_opportunities = core_helpers.filter_opportunities(
                filtered_opportunities,
                self.sector
            )

        if self.region.regions:
            filtered_opportunities = core_helpers.filter_opportunities(
                filtered_opportunities,
                self.region
            )

        if self.scale.selected_scales:
            filtered_opportunities = core_helpers.filter_opportunities(
                filtered_opportunities,
                self.scale
            )

        if self.sub_sector.sub_sectors:
            filtered_opportunities = core_helpers.filter_opportunities(
                filtered_opportunities,
                self.sub_sector
            )

        if self.planning_status.planning_statuses:
            filtered_opportunities = core_helpers.filter_opportunities(
                filtered_opportunities,
                self.planning_status
            )

        if self.investment_type.investment_types:
            filtered_opportunities = core_helpers.filter_opportunities(
                filtered_opportunities,
                self.investment_type
            )

        if self.sort_filter.sort_by_filter_chosen:
            filtered_opportunities = core_helpers.sort_opportunities(
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
        for investment_type in self.investment_type.investment_types:
            filters.append(investment_type)
        for planning_status in self.planning_status.planning_statuses:
            filters.append(planning_status)

        return filters

    @property
    def sorting_chosen(self):
        return self.sort_filter.sort_by_filter_chosen.title

    @property
    def opportunity_search_form(self):
        return forms.InvestmentOpportunitySearchForm(
            sectors=self.all_sectors,
            scales=self.all_scales,
            regions=self.all_regions,
            sort_by_options=self.all_sort_filters,
            sub_sectors=self.all_sub_sectors_for_sectors_chosen,
            investment_types=self.all_investment_types,
            planning_statuses=self.all_planning_statuses,
            initial={
                'sector': self.filters_chosen,
                'scale': self.filters_chosen,
                'region': self.filters_chosen,
                'sort_by': self.sorting_chosen,
                'sub_sector': self.filters_chosen,
                'planning_status': self.filters_chosen,
                'investment_type': self.filters_chosen,
            },
        )

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            num_of_opportunities=self.num_of_opportunities,
            sectors=self.all_sectors,
            scales=self.all_scales,
            regions=self.all_regions,
            sorting_filters=self.all_sort_filters,
            investment_types=self.all_investment_types,
            planning_statuses=self.all_planning_statuses,
            sub_sectors=self.all_sub_sectors_for_sectors_chosen,
            pagination=self.pagination,
            sorting_chosen=self.sorting_chosen,
            filters=self.filters_chosen,
            current_page_num=self.page_number,
            form=self.opportunity_search_form,
            *args, **kwargs,
        )
