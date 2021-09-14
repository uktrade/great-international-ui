import copy
import random

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView, View
from django.views.generic import TemplateView, FormView
from django.utils.functional import cached_property
from django.utils import translation
from django.urls import reverse_lazy

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response
import directory_forms_api_client.helpers

from directory_constants import urls
from directory_components.helpers import SocialLinkBuilder
from directory_components.mixins import (
    CMSLanguageSwitcherMixin, GA360Mixin, CountryDisplayMixin, EnableTranslationsMixin)

from core import forms, helpers, constants
from core.context_modifiers import register_context_modifier, registry as context_modifier_registry
from core.helpers import get_map_labels_with_vertical_positions, get_sender_ip_address
from core.mixins import NotFoundOnDisabledFeature, RegionalContentMixin, InternationalHeaderMixin
from core.templatetags.cms_tags import filter_by_active_language
from core.header_config import tier_one_nav_items, tier_two_nav_items

import find_a_supplier.forms
from investment_atlas.helpers import get_sectors_label


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
    def template_name(self):
        return 'investment_atlas/homepage.html'


@register_context_modifier('InternationalTopicLandingPage')
def sector_landing_page_context_modifier(context, request):
    child_pages_for_language = filter_by_active_language(context['page']['child_pages'])

    cards_list = [create_cards_list_item(
        x['full_path'],
        x['heading'],
        x['sub_heading'],
        x['hero_image_thumbnail']
    ) for x in child_pages_for_language]

    return {
        "cards_list": cards_list
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


class InternationalContactPageView(CountryDisplayMixin, InternationalView):
    template_name = 'core/contact_page.html'
    header_section = tier_one_nav_items.CONTACT

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


@register_context_modifier('CapitalInvestOpportunityPage')
def capital_invest_opportunity_page_context_modifier(context, request):
    current_sector_title = None
    related_sectors = context['page']['related_sectors']

    if related_sectors:
        current_sector_title = related_sectors[0]['related_sector']['title'].lower()

    return {
        'invest_cta_link': urls.international.EXPAND_HOME,
        'buy_cta_link': urls.international.TRADE_HOME,
        'current_sector_title': current_sector_title,
        'contact_cta_link': urls.international.CAPITAL_INVEST_CONTACT,
    }


class SendContactNotifyMessagesMixin:
    def send_company_message(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=None,
            ip_address=get_sender_ip_address(self.request),
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

    return {
        'international_home_page_link': urls.international.HOME,
        'investment_support_directory_link': urls.international.EXPAND_ISD_HOME,
        'how_to_set_up_visas_and_migration_link': urls.international.EXPAND_HOW_TO_SETUP_VISAS_AND_MIGRATION,
        'how_to_set_up_tax_and_incentives_link': urls.international.EXPAND_HOW_TO_SETUP_TAX_AND_INCENTIVES,
        'show_hpo_section': bool(hpo_pages and filter_by_active_language(hpo_pages[0])),
        'show_featured_cards': (number_of_featured_cards == 3),
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


def create_cards_list_item(url, title, summary, image):
    base_item = {
        'url': url,
        'title': title,
        'summary': summary,
    }

    if image:
        base_item.update({
            'image': image.get('url'),
            'image_alt': image.get('alt'),
            'image_width': image.get('width'),
            'image_height': image.get('height'),
        })

    return base_item


@register_context_modifier('AboutUkRegionListingPage')
@register_context_modifier('AboutUkRegionPage')
def about_uk_region_listing_page_context_modifier(context, request):
    regions = {}
    cards_list = []
    if 'mapped_regions' in context['page']:
        regions = {
            # variable names in templates can only contain underscores and letters/numbers:
            x['region']['meta']['slug'].replace('-', '_'): {
                'full_path': x['region']['full_path']
            }
            for x in context['page']['mapped_regions']
        }
        cards_list = [create_cards_list_item(
            x['region']['full_path'],
            x['region']['title'],
            x['text'],
            x['region'].get('hero_image_thumbnail')
        ) for x in context['page']['mapped_regions']]

    return {
        'regions': regions,
        'cards_list': cards_list
    }


@register_context_modifier('InvestmentOpportunityPage')
def atlas_opportunity_page_context_modifier(context, request):
    return {
        'sectors_label': get_sectors_label(context['page'])
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


class CapitalInvestContactFormView(MultilingualCMSPageFromPathView, GA360Mixin, FormView):
    form_class = forms.CapitalInvestContactForm
    success_url = '/international/content/capital-invest/contact/success'
    header_section = tier_one_nav_items.CONTACT

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

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            privacy_url=urls.domestic.PRIVACY_AND_COOKIES / 'fair-processing-notice-invest-in-great-britain/',
            *args, **kwargs)


class PathRedirectView(QuerystringRedirectView):
    root_url = None

    @property
    def url(self, **kwargs):
        path = self.kwargs['path']
        return f'{self.root_url}/{path}'


class BusinessEnvironmentGuideFormView(EnableTranslationsMixin, GA360Mixin, InternationalHeaderMixin, FormView):
    template_name = "core/investment_prospectus_form.html"
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
            country_code=form.cleaned_data['market'],
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

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            privacy_url=urls.domestic.PRIVACY_AND_COOKIES / 'privacy-notice-uk-investment-prospectus/',
            *args, **kwargs)


class BusinessEnvironmentGuideFormSuccessView(InternationalView):
    template_name = 'core/investment_prospectus_form_success.html'
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


class WhyBuyFromUKFormView(GA360Mixin, EnableTranslationsMixin, InternationalHeaderMixin, FormView):
    template_name = "core/why_buy_from_the_uk_form.html"
    form_class = forms.WhyBuyFromUKForm
    subject = "How we help Guide Form"
    success_url = reverse_lazy('why-buy-from-uk-form-success')
    header_section = tier_one_nav_items.BUY_FROM_THE_UK
    header_sub_section = tier_two_nav_items.HOW_WE_HELP_BUY

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='WhyBuyFromUKForm',
            business_unit='GreatInternational',
            site_section='Trade',
            site_subsection='HowWeHelp'
        )

    def send_agent_email(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=form.cleaned_data['market'],
        )
        response = form.save(
            form_url=self.request.get_full_path(),
            email_address=settings.HOW_WE_HELP_GUIDE_AGENT_EMAIL,
            template_id=settings.HOW_WE_HELP_GUIDE_AGENT_TEMPLATE_ID,
            sender=sender,
        )
        response.raise_for_status()

    def send_user_email(self, form):
        response = form.save(
            form_url=self.request.path,
            email_address=form.cleaned_data['email_address'],
            template_id=settings.HOW_WE_HELP_GUIDE_USER_TEMPLATE_ID,
            email_reply_to_id=settings.HOW_WE_HELP_GUIDE_REPLY_TO_ID
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_email(form)
        self.send_user_email(form)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            international_trade_home=urls.international.TRADE_HOME,
            international_trade_how_we_help=urls.international.TRADE_HOW_WE_HELP,
            privacy_url=urls.domestic.PRIVACY_AND_COOKIES / 'privacy-notice-5-reasons-buy-uk/',
            *args, **kwargs,
        )


class WhyBuyFromUKFormViewSuccess(InternationalView):
    template_name = 'core/why_buy_from_the_uk_form_success.html'
    page_type = 'HowWeHelpGuideFormViewSuccessPage'
    header_section = tier_one_nav_items.BUY_FROM_THE_UK
    header_sub_section = tier_two_nav_items.HOW_WE_HELP_BUY

    def dispatch(self, request, *args, **kwargs):
        self.set_ga360_payload(
            page_id='HowWeHelpGuideFormViewSuccessPage',
            business_unit='GreatInternational',
            site_section='Trade',
            site_subsection='HowWeHelp'
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            international_trade_home=urls.international.TRADE_HOME,
            international_trade_how_we_help=urls.international.TRADE_HOW_WE_HELP,
            *args, **kwargs,
        )


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '500.html', status=500)


class InternationalContactTriageView(
    GA360Mixin,
    EnableTranslationsMixin,
    InternationalHeaderMixin,
    FormView,
):
    template_name = 'core/contact_international_triage.html'
    form_class = forms.InternationalRoutingForm
    success_url = urls.domestic.CONTACT_US + 'international/'
    header_section = tier_one_nav_items.CONTACT

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
