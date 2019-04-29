from unittest.mock import patch
import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from django.utils import translation
from django.views.generic import TemplateView

from directory_components.mixins import CMSLanguageSwitcherMixin

from core.mixins import CMSPageMixin, GetSlugFromKwargsMixin
from core import helpers
from core.tests.helpers import create_response
from core.views import SectorPageCMSView


test_sectors = [
    {
        'title': 'Aerospace',
        'featured': True,
        'meta': {
            'slug': 'invest-aerospace',
            'languages': [
                ['en-gb', 'English'],
                ['ar', 'العربيّة'],
                ['de', 'Deutsch'],
            ],
        },
    },
    {
        'title': 'Automotive',
        'featured': True,
        'meta': {
            'slug': 'invest-automotive',
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['ja', '日本語'],
            ],
        },
    },
]

dummy_page = {
    'title': 'test',
    'meta': {
        'languages': [
            ['en-gb', 'English'],
            ['fr', 'Français'],
            ['de', 'Deutsch'],
        ]
    },
    'page_type': ''
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_language_switcher_one_language(mock_cms_response, rf):
    class MyView(CMSPageMixin, CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'
        slug = 'test'
        active_view_name = ''

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['de', 'Deutsch'],
            ]
        },
        'page_type': ''
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    request.LANGUAGE_CODE = 'de'

    response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_language_switcher_active_language_available(
    mock_cms_response, rf
):
    class MyView(CMSPageMixin, CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'
        slug = 'test'
        active_view_name = ''

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_active_view_name(mock_cms_response, rf):
    class TestView(CMSPageMixin, TemplateView):
        active_view_name = 'test'
        template_name = 'core/base.html'
        slug = 'test'

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['active_view_name'] == 'test'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_cms_page(mock_cms_response, rf):
    class TestView(CMSPageMixin, TemplateView):
        template_name = 'core/base.html'
        slug = 'invest-home-page'
        active_view_name = ''

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.context_data['page'] == dummy_page


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_cms_page_kwargs_slug(mock_cms_response, rf):
    class TestView(GetSlugFromKwargsMixin, CMSPageMixin, TemplateView):
        template_name = 'core/base.html'
        active_view_name = ''

    page = {
        'title': 'the page',
        'meta': {
            'languages': [('en-gb', 'English'), ('de', 'German')],
            'slug': 'aerospace'
        },
        'page_type': ''
    }

    mock_cms_response.return_value = helpers.create_response(
            status_code=200,
            json_payload=page
        )

    translation.activate('en-gb')
    request = rf.get('/')
    view = TestView.as_view()
    response = view(request, slug='aerospace')

    assert response.context_data['page'] == page


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_breadcrumbs_mixin(mock_get_page, client, settings):

    url = reverse('article-detail', kwargs={
        'topic': 'topic', 'list': 'bar', 'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'page_type': 'InternationalArticlePage',
            'meta': {
                'slug': 'foo',
                'languages': [('en-gb', 'English')],
            },
        }
    )
    response = client.get(url)

    breadcrumbs = response.context_data['breadcrumbs']
    assert breadcrumbs == [
        {
            'url': '/international/',
            'label': 'International'
        },
        {
            'url': '/international/topic/',
            'label': 'Topic'
        },
        {
            'url': '/international/topic/bar/',
            'label': 'Bar'
        },
        {
            'url': '/international/topic/bar/foo/',
            'label': 'Foo'
        },
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_article_detail_page_social_share_links(
    mock_get_page, client, settings
):

    test_article_page = {
        'title': 'Test article admin title',
        'article_title': 'Test article',
        'article_image': {'url': 'foobar.png'},
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [],
        'full_path': (
            '/international/topic/bar/foo/'),
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'slug': 'foo',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
    }

    url = reverse('article-detail', kwargs={
        'topic': 'topic', 'list': 'bar', 'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=test_article_page
    )

    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == ['core/article_detail.html']

    twitter_link = (
        'https://twitter.com/intent/tweet?text=great.gov.uk'
        '%20-%20Test%20article%20'
        'http://testserver/international/topic/bar/foo/')
    facebook_link = (
        'https://www.facebook.com/share.php?u='
        'http://testserver/international/topic/bar/foo/')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/international/topic/bar/foo/'
        '&title=great.gov.uk'
        '%20-%20Test%20article%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/international/topic/bar/'
        'foo/&subject=great.gov.uk%20-%20Test%20article%20'
    )

    assert soup.find(id='share-twitter').attrs['href'] == twitter_link
    assert soup.find(id='share-facebook').attrs['href'] == facebook_link
    assert soup.find(id='share-linkedin').attrs['href'] == linkedin_link
    assert soup.find(id='share-email').attrs['href'] == email_link


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_article_detail_page_social_share_links_no_title(
    mock_get_page, client, settings
):

    test_article_page = {
        'title': 'Test article admin title',
        'article_image': {'url': 'foobar.png'},
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [],
        'full_path': (
            '/international/bar/foo/'),
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'slug': 'foo',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
    }

    url = reverse('article-detail', kwargs={
        'topic': 'topic', 'list': 'bar', 'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=test_article_page
    )

    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == ['core/article_detail.html']

    twitter_link = (
        'https://twitter.com/intent/tweet?text=great.gov.uk%20-%20%20'
        'http://testserver/international/topic/bar/foo/'
        '')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/international/topic/bar/foo/'
        '&title=great.gov.uk'
        '%20-%20%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/international/topic/bar/'
        'foo/&subject='
        'great.gov.uk%20-%20%20'
    )

    assert soup.find(id='share-twitter').attrs['href'] == twitter_link
    assert soup.find(id='share-linkedin').attrs['href'] == linkedin_link
    assert soup.find(id='share-email').attrs['href'] == email_link


test_child_pages = [
    {
        'last_published_at': '2019-02-28T10:56:30.455848Z',
        'meta': {
            'slug': 'campaign-one',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalCampaignPage',
        'teaser': 'Campaign one teaser',
        'title': 'Campaign one'
    },
    {
        'last_published_at': '2019-02-28T10:56:31.455848Z',
        'meta': {
            'slug': 'article-one',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article one teaser',
        'title': 'Article one'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-two',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article two teaser',
        'title': 'Article two'
    },
]

test_localised_child_pages = [
    {
        'last_published_at': '2019-02-28T10:56:30.455848Z',
        'meta': {
            'slug': 'campaign-one',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalCampaignPage',
        'teaser': 'Campaign one teaser',
        'title': 'Campaign one'
    },
    {
        'last_published_at': '2019-02-28T10:56:31.455848Z',
        'meta': {
            'slug': 'article-one',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article one teaser',
        'title': 'Article one'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-two',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article two teaser',
        'title': 'Article two'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-three',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article three teaser',
        'title': 'Article three'
    },
]

test_list_page = {
    'title': 'List CMS admin title',
    'seo_title': 'SEO title article list',
    'search_description': 'Article list search description',
    'landing_page_title': 'Article list landing page title',
    'hero_image': {'url': 'article_list.png'},
    'hero_teaser': 'Article list hero teaser',
    'list_teaser': '<p>Article list teaser</p>',
    'child_pages': test_child_pages,
    'localised_child_pages': test_localised_child_pages,
    'page_type': 'InternationalArticleListingPage',
    'meta': {
        'slug': 'article-list',
        'languages': [('en-gb', 'English')],
    },
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_article_list_page(mock_get_page, client, settings):

    url = reverse('article-list', kwargs={
        'topic': 'article-topic',
        'slug': 'article-list'
    })

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=test_list_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/article_list.html']

    assert test_list_page['title'] not in str(response.content)
    assert test_list_page['landing_page_title'] in str(response.content)

    assert '28 February' in str(response.content)


@pytest.mark.parametrize('url,page_type,status_code', (
    (
        '/international/article-list/',
        'InternationalArticlePage',
        404
    ),
    (
        '/international/topic/list/article-page/',
        'InternationalArticlePage',
        200
    ),
    (
        '/international/topic/list/article-page/',
        'InternationalArticleListingPage',
        404
    ),
    (
        '/international/topic/list/',
        'InternationalArticleListingPage',
        200
    ),
    (
        '/international/topic/campaign/',
        'InternationalCampaignPage',
        404
    ),
    (
        '/international/campaigns/campaign/',
        'InternationalCampaignPage',
        200
    ),
    (
        '/international/',
        'InternationalArticlePage',
        404
    ),
    (
        '/international/',
        'InternationalHomePage',
        200
    ),
))
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_page_url_mismatch_404(
    mock_get_page, url, page_type, status_code, client
):
    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'page_type': page_type,
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
            # Needed to prevent errors when rendering some page types
            'localised_child_pages': [],
            'child_pages': [],
            'related_pages': [],
        }
    )

    response = client.get(url)
    assert response.status_code == status_code


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage_no_related_pages(mock_get_page, client):
    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'page_type': 'InternationalHomePage',
            'news_title': 'News title',
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
            'related_pages': []
        }
    )

    response = client.get(reverse('index'))
    assert 'News title' not in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage_related_pages(mock_get_page, client):
    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'page_type': 'InternationalHomePage',
            'news_title': 'News title',
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
            'related_pages': [
                {
                    'title': 'Related article title',
                    'page_type': 'InternationalArticlePage',
                    'teaser': 'Related article teaser',
                    'meta': {
                        'slug': 'article',
                        'languages': [('en-gb', 'English')],
                    },
                    'full_path': '/topic/list/article',
                    'full_url':
                    'https://great.gov.uk/international/topic/list/article',
                },
                {
                    'title': 'Related campaign title',
                    'page_type': 'InternationalCampaignPage',
                    'teaser': 'Related campaign teaser',
                    'meta': {
                        'slug': 'campaign',
                        'languages': [('en-gb', 'English')],
                    },
                    'full_path': '/international/campaigns/campaign',
                    'full_url':
                    'https://great.gov.uk/international/campaigns/campaign',
                },
            ]
        }
    )

    response = client.get(reverse('index'))
    assert 'News title' in str(response.content)
    assert 'Related article title' in str(response.content)
    assert 'Related article teaser' in str(response.content)
    assert '/topic/list/article' in str(response.content)
    assert 'Related campaign title' in str(response.content)
    assert 'Related campaign teaser' in str(response.content)
    assert '/international/campaigns/campaign' in str(response.content)


@pytest.mark.parametrize('localised_articles,total_articles', (
    (
        [],
        4
    ),
    (
        test_localised_child_pages[:-3],
        5
    ),
    (
        test_localised_child_pages,
        8
    ),
))
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_article_count_with_regional_articles(
    mock_get_page, localised_articles, total_articles, client
):
    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'page_type': 'InternationalArticleListingPage',
            'articles_count': 4,
            'localised_child_pages': localised_articles,
            'child_pages': [],
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
        }
    )
    url = reverse('article-list', kwargs={'topic': 'topic', 'slug': 'slug'})
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    assert '{} articles'.format(total_articles) in soup.find(
        id='hero-description').string


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_sector_page_attaches_array_lengths_to_view(mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'InternationalSectorPage',
        'statistics': [
            {'number': '1'},
            {'number': '2', 'heading': 'heading'},
            {'number': None, 'heading': 'no-number-stat'}
        ],
        'section_three_subsections': [
            {'heading': 'heading'},
            {'heading': 'heading-with-teaser', 'teaser': 'teaser'},
            {'heading': None, 'teaser': 'teaser-without-heading'}
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'
    response = SectorPageCMSView.as_view()(request)

    view = response.context_data['view']
    assert view.num_of_statistics == 2
    assert view.section_three_num_of_subsections == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_industries_page_renames_heading_to_landing_page_title(
    mock_get_page, client
):
    page = {
        'title': 'test',
        'page_type': 'InternationalTopicLandingPage',
        'child_pages': [
            {
                'heading': 'heading',
                'meta': {
                    'languages': [('en-gb', 'English')],
                },
            }
        ],
        'meta': {
            'slug': 'slug',
            'languages': [('en-gb', 'English')],
        }
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = reverse('industries')
    response = client.get(url)

    child_page = response.context_data['page']['child_pages'][0]
    assert child_page['landing_page_title'] == 'heading'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_how_to_do_business_feature_off(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = False

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=dummy_page
    )

    url = reverse('how-to-do-business-with-the-uk')

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_how_to_do_business_feature_on(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = True

    page = dummy_page
    page['page_type'] = 'InternationalCuratedTopicLandingPage'

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = reverse('how-to-do-business-with-the-uk')

    response = client.get(url)

    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_cms_page_from_path_view(lookup_by_path, client, settings):
    page = dummy_page.copy()
    page['page_type'] = 'InternationalCuratedTopicLandingPage'

    lookup_by_path.return_value = create_response(
        status_code=200,
        json_payload=page
    )
    response = client.get('/international/c/page/from/path')

    assert response.status_code == 200

    lookup_by_path.assert_called_with(
        draft_token=None,
        language_code='en-gb',
        path='page/from/path',
        site_id=settings.DIRECTORY_CMS_SITE_ID,
    )
