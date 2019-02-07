from unittest.mock import patch
import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from django.utils import translation
from django.http import Http404

from core.views import CMSPageView
from core.mixins import GetSlugFromKwargsMixin
from core import helpers
from core.tests.helpers import create_response


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
    }
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_language_switcher_one_language(mock_cms_response, rf):
    class MyView(CMSPageView):

        template_name = 'core/base.html'
        slug = 'test'
        active_view_name = ''

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['de', 'Deutsch'],
            ]
        }
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_language_switcher_active_language_available(
    mock_cms_response, rf
):
    class MyView(CMSPageView):

        template_name = 'core/base.html'
        slug = 'test'
        active_view_name = ''

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/de/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_active_view_name(mock_cms_response, rf):
    class TestView(CMSPageView):
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
    class TestView(CMSPageView):
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
    class TestView(GetSlugFromKwargsMixin, CMSPageView):
        template_name = 'core/base.html'
        active_view_name = ''

    page = {
        'title': 'the page',
        'meta': {
            'languages': [('en-gb', 'English'), ('de', 'German')],
            'slug': 'aerospace'
        },
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
def test_404_when_cms_language_unavailable(mock_cms_response, rf):
    class TestView(GetSlugFromKwargsMixin, CMSPageView):
        template_name = 'core/base.html'

    page = {
        'title': 'the page',
        'meta': {
            'languages': [('en-gb', 'English'), ('de', 'German')],
            'slug': 'aerospace'
        },
    }

    mock_cms_response.return_value = helpers.create_response(
            status_code=200,
            json_payload=page
        )

    translation.activate('fr')
    request = rf.get('/fr/')
    view = TestView.as_view()

    with pytest.raises(Http404):
        view(request, slug='aerospace')


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_article_article_detail_page_no_related_content(
    mock_get_page, client, settings
):
    test_article_page_no_related_content = {
        'title': 'Test article admin title',
        'article_title': 'Test article',
        'article_teaser': 'Test teaser',
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [],
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'languages': [('en-gb', 'English')],
            'slug': 'foo',
        },
        'page_type': 'ArticlePage',
    }

    url = reverse(
        'article-detail',
        kwargs={'slug': 'foo'}
    )

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=test_article_page_no_related_content
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/article_detail.html']

    assert 'Related content' not in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_article_detail_page_related_content(
    mock_get_page, client, settings
):

    article_page = {
        'title': 'Test article admin title',
        'article_title': 'Test article',
        'article_teaser': 'Test teaser',
        'article_image': {'url': 'foobar.png'},
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [
            {
                'article_title': 'Related article 1',
                'article_teaser': 'Related article 1 teaser',
                'article_image_thumbnail': {'url': 'related_article_one.jpg'},
                'full_path': '/test-one',
                'meta': {
                    'slug': 'test-one',
                }
            },
            {
                'article_title': 'Related article 2',
                'article_teaser': 'Related article 2 teaser',
                'article_image_thumbnail': {'url': 'related_article_two.jpg'},
                'full_path': '/test-two',
                'meta': {
                    'slug': 'test-two',
                }
            },
        ],
        'meta': {
            'languages': [('en-gb', 'English')],
            'slug': 'bar',
        },
        'page_type': 'ArticlePage',
    }

    url = reverse(
        'article-detail',
        kwargs={'slug': 'foo'}
    )

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/article_detail.html']

    assert 'Related content' in str(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.find(
        id='related-article-test-one-link'
    ).attrs['href'] == '/international/test-one/'
    assert soup.find(
        id='related-article-test-two-link'
    ).attrs['href'] == '/international/test-two/'

    assert soup.find(
        id='related-article-test-one'
    ).select('h3')[0].text == 'Related article 1'
    assert soup.find(
        id='related-article-test-two'
    ).select('h3')[0].text == 'Related article 2'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_breadcrumbs_mixin(mock_get_page, client, settings):

    url = reverse('article-detail', kwargs={'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'page_type': 'ArticlePage',
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
            'url': '/international/foo/',
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
            '/international/foo/'),
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'slug': 'foo',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'ArticlePage',
    }

    url = reverse('article-detail', kwargs={'slug': 'foo'})

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
        'http://testserver/international/foo/')
    facebook_link = (
        'https://www.facebook.com/share.php?u=http://testserver/'
        'international/foo/')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/international/foo/&title=great.gov.uk'
        '%20-%20Test%20article%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/international/'
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
            '/international/foo/'),
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'slug': 'foo',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'ArticlePage',
    }

    url = reverse('article-detail', kwargs={'slug': 'foo'})

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
        'http://testserver/international/foo/'
        '')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/international/foo/'
        '&title=great.gov.uk'
        '%20-%20%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/international/'
        'foo/&subject='
        'great.gov.uk%20-%20%20'
    )

    assert soup.find(id='share-twitter').attrs['href'] == twitter_link
    assert soup.find(id='share-linkedin').attrs['href'] == linkedin_link
    assert soup.find(id='share-email').attrs['href'] == email_link
