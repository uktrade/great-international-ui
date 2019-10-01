import copy
import random

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView, View
from django.views.generic import TemplateView, FormView
from django.utils.functional import cached_property
from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response
import directory_forms_api_client.helpers

from directory_constants.choices import COUNTRY_CHOICES
from directory_constants import urls
from directory_components.helpers import get_user_country, SocialLinkBuilder
from directory_components.mixins import CMSLanguageSwitcherMixin, GA360Mixin, CountryDisplayMixin


from core import forms, helpers, constants
from core.context_modifiers import register_context_modifier, registry as context_modifier_registry
from core.helpers import get_map_labels_with_vertical_positions
from core.mixins import NotFoundOnDisabledFeature, RegionalContentMixin, InternationalHeaderMixin
from core.templatetags.cms_tags import filter_by_active_language
from core.header_config import tier_one_nav_items, tier_two_nav_items

import find_a_supplier.forms


class QuerystringRedirectView(RedirectView):
    query_string = True


class InternationalView(InternationalHeaderMixin, GA360Mixin, TemplateView):
    pass


class MonolingualCMSPageFromPathView(
    RegionalContentMixin,
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
    def page_type(self):
        return self.page['page_type']

    @property
    def path(self):
        return self.kwargs['path']

    @property
    def template_name(self):
        return constants.TEMPLATE_MAPPING[self.page_type]

    @property
    def header_section(self):
        return helpers.get_header_section(self.path)

    @property
    def header_sub_section(self):
        return helpers.get_header_sub_section(self.path)

    def get_cms_data(self, path):
        return cms_api_client.lookup_by_path(
                    site_id=self.cms_site_id,
                    path=path,
                    language_code=translation.get_language(),
                    draft_token=self.request.GET.get('draft_token'),
                )

    @cached_property
    def page(self):
        response = self.get_cms_data(self.path)

        if response.status_code == 404 and 'invest' in self.path:
            new_path = self.path.replace('invest', 'expand')
            response = self.get_cms_data(new_path)

        if response.status_code == 404 and 'how-to-setup-in-the-uk' in self.path:
            new_path = self.path.replace('how-to-setup-in-the-uk', 'invest/how-to-setup-in-the-uk')
            response = self.get_cms_data(new_path)

        if response.status_code == 404 and 'how-to-setup-in-the-uk' in self.path:
            new_path = self.path.replace('how-to-setup-in-the-uk', 'expand/how-to-setup-in-the-uk')
            response = self.get_cms_data(new_path)

        if response.status_code == 404 and 'industries' in self.path:
            new_path = self.path.replace('industries', 'about-uk/industries')
            response = self.get_cms_data(new_path)

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

        if not settings.FEATURE_FLAGS['ABOUT_UK_LANDING_PAGE_ON'] and 'tree_based_breadcrumbs' in self.page:
            self.page['tree_based_breadcrumbs'] = [crumb for crumb in self.page['tree_based_breadcrumbs']
                                                   if not crumb['url'].endswith('/international/content/about-uk/')]

        return context


class MultilingualCMSPageFromPathView(
    CMSLanguageSwitcherMixin, MonolingualCMSPageFromPathView
):
    pass


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


class InternationalHomePageView(MultilingualCMSPageFromPathView):

    @property
    def is_new_page_ready(self):
        if 'is_new_page_ready' in self.page:
            if self.page['is_new_page_ready']:
                return True
        return False

    @property
    def template_name(self):
        if self.is_new_page_ready:
            return 'core/new_international_landing_page.html'

        return 'core/landing_page.html'

    def get_context_data(self, *args, **kwargs):
        page = self.page

        country_code = get_user_country(self.request)
        country_name = dict(COUNTRY_CHOICES).get(country_code, '')
        tariffs_country = {'code': country_code.lower(), 'name': country_name}
        tariffs_country_selector_form = forms.TariffsCountryForm(
            initial={'tariffs_country': country_code}
        ),

        random_sector = []
        if 'all_sectors' in page:
            all_sectors = filter_by_active_language(page['all_sectors'])
            random.shuffle(all_sectors)
            if all_sectors:
                random_sector = all_sectors[0]

        related_cards = []
        if 'related_page_expand' in page and page['related_page_expand']:
            related_cards.append(page['related_page_expand'])

        if 'related_page_invest_capital' in page and page['related_page_invest_capital']:
            related_cards.append(page['related_page_invest_capital'])

        if 'related_page_buy' in page and page['related_page_buy']:
            related_cards.append(page['related_page_buy'])

        return super().get_context_data(
            tariffs_country=tariffs_country,
            tariffs_country_selector_form=tariffs_country_selector_form,
            random_sector=random_sector,
            related_cards=related_cards,
            *args, **kwargs,
        )


@register_context_modifier('InternationalTopicLandingPage')
def sector_landing_page_context_modifier(context, request):

    def rename_heading_field(page):
        page['landing_page_title'] = page['heading']
        return page

    context['page']['child_pages'] = [
        rename_heading_field(child_page)
        for child_page in context['page']['child_pages']]

    context['about_uk_link'] = urls.international.ABOUT_UK_HOME
    return context


@register_context_modifier('InternationalSectorPage')
def sector_page_context_modifier(context, request):
    page = context['page']

    if 'related_opportunities' in page:
        random.shuffle(page['related_opportunities'])
        random_opportunities = page['related_opportunities'][0:3]
    else:
        random_opportunities = []

    return {
        'invest_contact_us_url': urls.international.EXPAND_CONTACT,
        'num_of_statistics': helpers.count_data_with_field(
            page['statistics'], 'number'),
        'section_three_num_of_subsections': helpers.count_data_with_field(
            page['section_three_subsections'], 'heading'),
        'random_opportunities': random_opportunities,
        'trade_contact_form_url': urls.international.TRADE_CONTACT,
        'about_uk_link': urls.international.ABOUT_UK_HOME
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
        ),
        'about_uk_link': urls.international.ABOUT_UK_HOME
    }


@register_context_modifier('InternationalSubSectorPage')
def sub_sector_context_modifier(context, request):
    page = context['page']

    if 'related_opportunities' in page:
        random.shuffle(page['related_opportunities'])
        random_opportunities = page['related_opportunities'][0:3]
    else:
        random_opportunities = []

    return {
        'invest_contact_us_url': urls.international.EXPAND_CONTACT,
        'num_of_statistics': helpers.count_data_with_field(
            page['statistics'], 'number'),
        'section_three_num_of_subsections': helpers.count_data_with_field(
            page['section_three_subsections'], 'heading'),
        'random_opportunities': random_opportunities,
        'trade_contact_form_url': urls.international.TRADE_CONTACT
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
            invest_contact_us_url=urls.international.EXPAND_CONTACT,
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
        'show_accordions': show_accordions
    }


@register_context_modifier('AboutUkRegionPage')
def about_uk_region_page_context_modifier(context, request):
    page = context['page']

    show_mapped_regions = False
    regions = []
    if 'mapped_regions' in page:
        regions = page['mapped_regions']
        show_mapped_regions = True if len(regions) == 6 else False

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
        'show_accordions': show_accordions,
        'show_mapped_regions': show_mapped_regions,
        'regions': regions
    }


@register_context_modifier('CapitalInvestOpportunityPage')
def capital_invest_opportunity_page_context_modifier(context, request):

    page = context['page']
    random_sector = ''
    opps_in_random_sector = []

    if 'related_sectors' in page and page['related_sectors'] and any(page['related_sectors']):
        sectors = [sector['related_sector']['heading']
                   for sector in page['related_sectors']
                   if sector['related_sector']]
        random.shuffle(sectors)
        if sectors:
            random_sector = sectors[0]

    if 'related_sector_with_opportunities' in page \
            and page['related_sector_with_opportunities']:
        opps_in_random_sector = \
            page['related_sector_with_opportunities'][random_sector]
        random.shuffle(opps_in_random_sector)

    return {
        'invest_cta_link': urls.international.EXPAND_HOME,
        'buy_cta_link': urls.international.TRADE_HOME,
        'random_related_sector_title': random_sector,
        'random_opps_in_random_related_sector': opps_in_random_sector[0:3]
    }


class OpportunitySearchView(
    CountryDisplayMixin,
    InternationalView
):
    template_name = 'core/capital_invest/capital_invest_opportunity_listing_page.html'
    page_size = 10
    header_section = tier_one_nav_items.INVEST_CAPITAL
    header_sub_section = tier_two_nav_items.INVESTMENT_OPPORTUNITIES

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
            url = helpers.get_paginator_url(self.request.GET, 'opportunities') + "&page=1"
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
            invest_url=urls.international.EXPAND_HOME,
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


class SendContactNotifyMessagesMixin:

    def send_company_message(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=None,
        )
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['subject'], form.cleaned_data['body']]
        )

        response = form.save(
            template_id=self.notify_settings.company_template,
            email_address=self.company['email_address'],
            form_url=self.request.path,
            sender=sender,
            spam_control=spam_control,
        )
        response.raise_for_status()

    def send_support_message(self, form):
        response = form.save(
            template_id=self.notify_settings.support_template,
            email_address=self.notify_settings.support_email_address,
            form_url=self.request.get_full_path(),
        )
        response.raise_for_status()

    def send_investor_message(self, form):
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['subject'], form.cleaned_data['body']]
        )
        response = form.save(
            template_id=self.notify_settings.investor_template,
            email_address=form.cleaned_data['email_address'],
            form_url=self.request.get_full_path(),
            spam_control=spam_control,
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_company_message(form)
        self.send_support_message(form)
        self.send_investor_message(form)
        return super().form_valid(form)


class BaseNotifyFormView(SendContactNotifyMessagesMixin, FormView):
    pass


@register_context_modifier('InvestInternationalHomePage')
def invest_homepage_context_modifier(context, request):

    hpo_pages = []
    if 'high_potential_opportunities' in context['page']:
        hpo_pages = context['page']['high_potential_opportunities'],

    featured_cards = []
    if 'featured_cards' in context['page']:
        featured_cards = [card for card in context['page']['featured_cards']
                          if card['title'] and card['summary'] and card['image']]
    number_of_featured_cards = len(featured_cards)

    how_to_expand_items = []
    if 'how_to_expand' in context['page']:
        how_to_expand_items = [
            {'title': how_to['title'], 'text': how_to['text']}
            for how_to in context['page']['how_to_expand'] if how_to['title'] and how_to['text']
        ]

    return {
        'international_home_page_link': urls.international.HOME,
        'investment_support_directory_link': urls.international.EXPAND_ISD_HOME,
        'how_to_set_up_visas_and_migration_link': urls.international.EXPAND_HOW_TO_SETUP_VISAS_AND_MIGRATION,
        'how_to_set_up_tax_and_incentives_link': urls.international.EXPAND_HOW_TO_SETUP_TAX_AND_INCENTIVES,
        'show_hpo_section': bool(hpo_pages and filter_by_active_language(hpo_pages[0])),
        'show_featured_cards': (number_of_featured_cards == 3),
        'how_to_expand_items': how_to_expand_items,
        'how_to_expand_items_length': len(how_to_expand_items),
    }


@register_context_modifier('InternationalTradeHomePage')
def international_trade_homepage_context_modifier(context, request):

    return {
        'search_form': find_a_supplier.forms.SearchForm,
    }


REGION_MIDDLE_POINTS = {
    'scotland': {'x': 164, 'y': 206},
    'northern-ireland': {'x': 195, 'y': 372.5},
    'north-england': {'x': 440, 'y': 427.5},
    'wales': {'x': 333, 'y': 643},
    'midlands': {'x': 445, 'y': 582.5},
    'south-england': {'x': 485, 'y': 688.5},
}


def get_regions_with_coordinates(regions):
    regions_with_coordinates = {}

    for field in regions:
        title = field['region']['title']
        slug = field['region']['meta']['slug']

        regions_with_coordinates[slug] = get_map_labels_with_vertical_positions(
            title.split(), REGION_MIDDLE_POINTS[slug]['x'], REGION_MIDDLE_POINTS[slug]['y']
        )

    return regions_with_coordinates


@register_context_modifier('AboutUkLandingPage')
def about_uk_landing_page_context_modifier(context, request):

    regions = []
    if 'regions' in context['page']:
        regions = context['page']['regions']

    random_sectors = []
    if 'all_sectors' in context['page']:
        all_sectors = context['page']['all_sectors']
        random.shuffle(all_sectors)
        random_sectors = all_sectors[0:3]

    regions_with_coordinates = {
        'scotland': [],
        'northern-ireland': [],
        'north-england': [],
        'wales': [],
        'midlands': [],
        'south-england': []
    }

    show_regions = False
    if regions:
        region_pages = [field['region'] for field in regions if field['region']]
        regions_with_text = [field for field in regions
                             if field['region'] and field['text']]
        if len(regions_with_text) == 6 and len(filter_by_active_language(region_pages)) == 6:
            show_regions = True
            regions_with_coordinates = get_regions_with_coordinates(context['page']['regions'])

    return {
        'random_sectors': random_sectors,
        'show_regions': show_regions,
        'scotland': regions_with_coordinates['scotland'],
        'northern_ireland': regions_with_coordinates['northern-ireland'],
        'north_england': regions_with_coordinates['north-england'],
        'wales': regions_with_coordinates['wales'],
        'midlands': regions_with_coordinates['midlands'],
        'south_england': regions_with_coordinates['south-england'],
        'regions_with_points': regions_with_coordinates,
        'regions': regions
    }


@register_context_modifier('AboutUkRegionListingPage')
def about_uk_region_listing_page_context_modifier(context, request):

    regions = []
    if 'mapped_regions' in context['page']:
        regions = context['page']['mapped_regions']

    regions_with_coordinates = {
        'scotland': [],
        'northern-ireland': [],
        'north-england': [],
        'wales': [],
        'midlands': [],
        'south-england': []
    }

    show_mapped_regions = False
    if regions:
        region_pages = [field['region'] for field in regions if field['region']]
        regions_with_text = [field for field in regions
                             if field['region'] and field['text']]
        if len(regions_with_text) == 6 and len(filter_by_active_language(region_pages)) == 6:
            show_mapped_regions = True
            regions_with_coordinates = get_regions_with_coordinates(regions)

    return {
        'show_mapped_regions': show_mapped_regions,
        'scotland': regions_with_coordinates['scotland'],
        'northern_ireland': regions_with_coordinates['northern-ireland'],
        'north_england': regions_with_coordinates['north-england'],
        'wales': regions_with_coordinates['wales'],
        'midlands': regions_with_coordinates['midlands'],
        'south_england': regions_with_coordinates['south-england'],
        'regions_with_points': regions_with_coordinates,
        'regions': regions
    }


class LegacyRedirectCoreView(View):
    http_method_names = ['get']
    redirects_mapping = {}
    fallback_url = None

    @staticmethod
    def translate_language_from_path_to_querystring(path, params):
        return path, params

    def get(self, request, path, *args, **kwargs):
        path = self._normalise_path(path)
        params = copy.deepcopy(request.GET)
        path, params = self.translate_language_from_path_to_querystring(path, params)
        destination = self.redirects_mapping.get(path) or self.fallback_url
        if params:
            destination = f'{destination}?{params.urlencode()}'
        return redirect(destination)

    @staticmethod
    def _normalise_path(path):
        """
        Make sure path is lowercase without the / at the ends
        """
        path = path.lower()
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        return path


class CapitalInvestContactFormView(
    MultilingualCMSPageFromPathView,
    GA360Mixin,
    FormView,
):
    form_class = forms.CapitalInvestContactForm
    success_url = '/international/content/capital-invest/contact/success'
    header_section = tier_one_nav_items.INVEST_CAPITAL
    header_sub_section = tier_two_nav_items.CONTACT_US_INVEST_CAPITAL

    def send_agent_email(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=form.cleaned_data['country'],
        )
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['message']]
        )
        response = form.save(
            form_url=self.request.path,
            email_address=settings.CAPITAL_INVEST_CONTACT_EMAIL,
            template_id=settings.CAPITAL_INVEST_AGENT_TEMPLATE_ID,
            sender=sender,
            spam_control=spam_control,
        )
        response.raise_for_status()

    def send_user_email(self, form):
        response = form.save(
            form_url=self.request.path,
            email_address=form.cleaned_data['email_address'],
            template_id=settings.CAPITAL_INVEST_USER_TEMPLATE_ID,
            email_reply_to_id=settings.CAPITAL_INVEST_USER_REPLY_TO_ID
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_email(form)
        self.send_user_email(form)
        return super().form_valid(form)


class PathRedirectView(QuerystringRedirectView):

    root_url = None

    @property
    def url(self, **kwargs):
        path = self.kwargs['path']
        return f'{self.root_url}/{path}'


class BusinessEnvironmentGuideFormView(GA360Mixin, InternationalHeaderMixin, FormView):
    template_name = "core/business_environment_guide_form.html"
    form_class = forms.BusinessEnvironmentGuideForm
    subject = "Business Environment Guide Form"
    success_url = '/international/about-uk/why-choose-uk/business-environment-guide/success/'
    header_section = tier_one_nav_items.ABOUT_UK
    header_sub_section = tier_two_nav_items.WHY_CHOOSE_THE_UK

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='BusinessEnvironmentForm',
            business_unit='GreatInternational',
            site_section='AboutUk',
            site_subsection='BusinessEnvironment'
        )

    def send_agent_email(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=form.cleaned_data['country'],
        )
        response = form.save(
            form_url=self.request.path,
            email_address=settings.GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_EMAIL,
            template_id=settings.GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_TEMPLATE_ID,
            sender=sender,
        )
        response.raise_for_status()

    def send_user_email(self, form):
        response = form.save(
            form_url=self.request.path,
            email_address=form.cleaned_data['email_address'],
            template_id=settings.GUIDE_TO_UK_BUSINESS_ENVIRONMENT_USER_TEMPLATE_ID,
            email_reply_to_id=settings.GUIDE_TO_UK_BUSINESS_ENVIRONMENT_REPLY_TO_ID
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_email(form)
        self.send_user_email(form)
        return super().form_valid(form)


class BusinessEnvironmentGuideFormSuccessView(InternationalView):
    template_name = 'core/business_environment_guide_form_success.html'
    page_type = 'BusinessEnvironmentGuideFormSuccessPage'
    header_section = tier_one_nav_items.ABOUT_UK
    header_sub_section = tier_two_nav_items.WHY_CHOOSE_THE_UK

    def dispatch(self, request, *args, **kwargs):
        self.set_ga360_payload(
            page_id='BusinessEnvironmentGuideFormSuccessPage',
            business_unit='GreatInternational',
            site_section='AboutUk',
            site_subsection='BusinessEnvironment'
        )
        return super().dispatch(request, *args, **kwargs)


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '500.html', status=500)


class InternationalContactTriageView(GA360Mixin, InternationalHeaderMixin, FormView):
    template_name = 'core/contact_international_triage.html'
    form_class = forms.InternationalRoutingForm
    success_url = urls.domestic.CONTACT_US + 'international/'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='GreatInternationalContactTriage',
            business_unit='GreatInternational',
            site_section='GreatInternational',
            site_subsection='ContactTriage'
        )

    def form_valid(self, form):
        return redirect(form.cleaned_data['choice'])

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            domestic_contact_home=urls.domestic.CONTACT_US,
            *args, **kwargs,
        )
