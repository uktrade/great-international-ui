from django.utils.functional import cached_property
from django.utils.cache import set_response_etag
from django.utils import translation
from django.http import Http404

from directory_components.helpers import SocialLinkBuilder

from directory_constants.constants.choices import COUNTRY_CHOICES, EU_COUNTRIES

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response

from core import helpers
from core import forms


TEMPLATE_MAPPING = {
    'InternationalHomePage': 'core/landing_page.html',
    'InternationalTopicLandingPage': 'core/topic_list.html',
    'InternationalArticleListingPage': 'core/article_list.html',
    'InternationalArticlePage': 'core/article_detail.html',
    'InternationalCampaignPage': 'core/campaign.html',
    'InternationalSectorPage': 'core/sector_page.html',
    'InternationalCuratedTopicLandingPage': 'core/curated_topic_landing_page.html',  #noqa
}


class RegionalContentMixin:
    country_form_class = forms.CountryForm

    @property
    def region(self):
        country_code = helpers.get_user_country(self.request).upper() or None
        if country_code in EU_COUNTRIES:
            return 'eu'

    def get_context_data(self, *args, **kwargs):
        country_code = helpers.get_user_country(self.request)

        # if there is a country already detected we can hide the selector
        hide_country_selector = bool(country_code)
        country_name = dict(COUNTRY_CHOICES).get(country_code, '')

        country = {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }

        country_form_kwargs = self.get_country_form_kwargs()

        return super().get_context_data(
            hide_country_selector=hide_country_selector,
            country=country,
            form=self.country_form_class(**country_form_kwargs),
            region=self.region,
            *args, **kwargs
        )

    def get_country_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_country_form_initial_data(self.request),
            **kwargs,
        }


class CMSPageMixin:
    active_view_name = ''
    page_type = ''
    region = ''

    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]

    def dispatch(self, request, *args, **kwargs):
        """
        Avoid showing the wrong page type at the wrong url

        e.g. /international/topic-slug should be a topic page
        this avoids /international/article-slug showing an article page
        at a url where it shouldn't exist
        """

        if self.page['page_type'] != self.page_type:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            region=self.region,
            draft_token=self.request.GET.get('draft_token'),
        )
        return self.handle_cms_response(response)

    def handle_cms_response(self, response):
        page = handle_cms_response(response)
        requested_language = translation.get_language()
        if requested_language not in dict(page['meta']['languages']):
            raise Http404('Content not found in requested language.')
        return page

    def get_context_data(self, *args, **kwargs):
        page = self.page
        show_language_switcher = (
            len(page['meta']['languages']) > 1 and
            'en-gb' in page['meta']['languages'][0]
        )
        language_available = translation.get_language() \
            in page['meta']['languages']

        return super().get_context_data(
            language_switcher={
                'show': show_language_switcher,
                'available_languages': page['meta']['languages'],
                'language_available': language_available
            },
            page=page,
            active_view_name=self.active_view_name,
            *args,
            **kwargs
        )


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class GetSlugFromKwargsMixin:
    @property
    def slug(self):
        return self.kwargs.get('slug')


class ArticleSocialLinksMixin:

    @property
    def page_title(self):
        return self.page.get('article_title', '')

    def get_context_data(self, *args, **kwargs):

        social_links_builder = SocialLinkBuilder(
            self.request.build_absolute_uri(),
            self.page_title,
            'great.gov.uk')

        return super().get_context_data(
            social_links=social_links_builder.links,
            *args, **kwargs
        )


class BreadcrumbsMixin:

    def get_context_data(self, *args, **kwargs):
        parts = self.request.path.split('/')
        url_fragments = [part for part in parts if part]

        breadcrumbs = []

        for index, slug in enumerate(url_fragments):
            url = '/'.join(url_fragments[0:index+1])
            breadcrumb = {
                'url': '/' + url + '/',
                'label': helpers.unslugify(slug)
            }
            breadcrumbs.append(breadcrumb)

        return super().get_context_data(
            breadcrumbs=breadcrumbs,
            *args, **kwargs
        )
