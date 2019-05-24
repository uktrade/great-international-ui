from unittest.mock import patch
from bs4 import BeautifulSoup

from django.urls import reverse

from core import helpers
from core.tests.helpers import create_response
from core.views import CMSPageFromPathView
from directory_constants import urls


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


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_cms_language_switcher_one_language(mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'InternationalHomePage'
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/')
    request.LANGUAGE_CODE = 'de'

    response = CMSPageFromPathView.as_view()(request, path='/international/')

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_cms_language_switcher_active_language_available(
    mock_cms_response, rf
):
    page = dummy_page.copy()
    page['page_type'] = 'InternationalHomePage'

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = CMSPageFromPathView.as_view()(request, path='/international/')

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_cms_page(mock_cms_response, rf):

    page = dummy_page.copy()
    page['page_type'] = 'InternationalHomePage'

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(request, path='/')

    assert response.context_data['page'] == page


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
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
            '/international/content/topic/bar/foo/'),
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'slug': 'foo',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
    }

    url = '/international/content/topic/bar/foo/'

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
        'http://testserver/international/content/topic/bar/foo/')
    facebook_link = (
        'https://www.facebook.com/share.php?u='
        'http://testserver/international/content/topic/bar/foo/')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/international/content/topic/bar/foo/'
        '&title=great.gov.uk'
        '%20-%20Test%20article%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/international/content/topic/bar/'
        'foo/&subject=great.gov.uk%20-%20Test%20article%20'
    )

    assert soup.find(id='share-twitter').attrs['href'] == twitter_link
    assert soup.find(id='share-facebook').attrs['href'] == facebook_link
    assert soup.find(id='share-linkedin').attrs['href'] == linkedin_link
    assert soup.find(id='share-email').attrs['href'] == email_link


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_article_detail_page_social_share_links_no_title(
    mock_get_page, client, settings
):

    test_article_page = {
        'title': 'Test article admin title',
        'article_image': {'url': 'foobar.png'},
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [],
        'full_path': (
            '/international/content/topic/bar/foo/'),
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'slug': 'foo',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
    }

    url = '/international/content/topic/bar/foo/'

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
        'http://testserver/international/content/topic/bar/foo/'
        '')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/international/content/topic/bar/foo/'
        '&title=great.gov.uk'
        '%20-%20%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/international/content/topic/bar/'
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


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
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

    request = rf.get('/international/content/industries/sector-page/')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/industries/sector-page/')

    assert response.context_data['num_of_statistics'] == 2
    assert response.context_data['section_three_num_of_subsections'] == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
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


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_how_to_do_business_feature_off(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = False

    mock_get_page.return_value = create_response(json_payload={
        **dummy_page, 'page_type': 'InternationalCuratedTopicLandingPage'
    })

    response = client.get(reverse('how-to-do-business-with-the-uk'))

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_how_to_do_business_feature_on(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = True

    mock_get_page.return_value = create_response(json_payload={
        **dummy_page, 'page_type': 'InternationalCuratedTopicLandingPage'
    })

    response = client.get(reverse('how-to-do-business-with-the-uk'))

    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_how_to_do_business_show_isd_english(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = True
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_LINK_ON'] = True

    mock_get_page.return_value = create_response(json_payload={
        **dummy_page, 'page_type': 'InternationalCuratedTopicLandingPage'
    })
    url = reverse('how-to-do-business-with-the-uk')

    response = client.get(url, {'lang': settings.LANGUAGE_CODE})

    assert response.status_code == 200
    assert response.context_data['is_english_selected'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_how_to_do_business_show_isd(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = True
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_LINK_ON'] = True

    mock_get_page.return_value = create_response(json_payload={
        **dummy_page, 'page_type': 'InternationalCuratedTopicLandingPage'
    })

    response = client.get(reverse('how-to-do-business-with-the-uk'))

    assert response.status_code == 200
    assert response.context_data['is_english_selected'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_how_to_do_business_hide_isd(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = True

    mock_get_page.return_value = create_response(json_payload={
        **dummy_page, 'page_type': 'InternationalCuratedTopicLandingPage'
    })
    url = reverse('how-to-do-business-with-the-uk')

    response = client.get(url, {'lang': 'fr'})

    assert response.status_code == 200
    assert response.context_data['is_english_selected'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_cms_page_from_path_view(lookup_by_path, client, settings):
    lookup_by_path.return_value = create_response(json_payload={
        **dummy_page, 'page_type': 'InternationalCuratedTopicLandingPage'
    })

    response = client.get('/international/content/page/from/path/')

    assert response.status_code == 200

    lookup_by_path.assert_called_with(
        draft_token=None,
        language_code='en-gb',
        path='page/from/path',
        site_id=settings.DIRECTORY_CMS_SITE_ID,
    )


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_capital_invest_region_page_attaches_array_lengths_to_view(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'CapitalInvestRegionPage',
        'economics_stats': [
            {'number': '1'},
            {'number': '2', 'heading': 'heading'},
            {'number': None, 'heading': 'no-number-stat'}
        ],
        'location_stats': [
            {'number': '1'},
            {'number': None, 'heading': 'no-number-stat'}
        ],
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/capital-invest/')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/capital-invest/')

    assert response.context_data['num_of_economics_statistics'] == 2
    assert response.context_data['num_of_location_statistics'] == 1


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_capital_invest_regional_sector_page_url_constants(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'CapitalInvestRegionalSectorPage'
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/midlands/')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/midlands/')

    assert response.context_data['invest_cta_link'] == urls.SERVICES_INVEST
    assert response.context_data['buy_cta_link'] == urls.SERVICES_FAS


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_capital_invest_opportunity_page_url_constants(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'CapitalInvestOpportunityPage'
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/ashton')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/opportunities/ashton')

    assert response.context_data['invest_cta_link'] == urls.SERVICES_INVEST
    assert response.context_data['buy_cta_link'] == urls.SERVICES_FAS


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_landing_page_returns_404_when_feature_flag_off(
        mock_get_page, client, settings
):

    settings.FEATURE_FLAGS['CAPITAL_INVEST_LANDING_PAGE_ON'] = False

    page = dummy_page.copy()
    page['page_type'] = 'InternationalCapitalInvestLandingPage'

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = '/international/content/capital-invest/'

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_region_page_returns_404_when_feature_flag_off(
        mock_get_page, client, settings
):

    settings.FEATURE_FLAGS['CAPITAL_INVEST_REGION_SECTOR_OPP_PAGES_ON'] = False

    page = dummy_page.copy()
    page['page_type'] = 'CapitalInvestRegionPage'

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = '/international/content/midlands/'

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_sector_page_returns_404_when_feature_flag_off(
        mock_get_page, client, settings
):

    settings.FEATURE_FLAGS['CAPITAL_INVEST_REGION_SECTOR_OPP_PAGES_ON'] = False

    page = dummy_page.copy()
    page['page_type'] = 'CapitalInvestRegionalSectorPage'

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = '/international/content/midlands/housing/'

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_opportunity_page_returns_404_when_feature_flag_off(
        mock_get_page, client, settings
):

    settings.FEATURE_FLAGS['CAPITAL_INVEST_REGION_SECTOR_OPP_PAGES_ON'] = False

    page = dummy_page.copy()
    page['page_type'] = 'CapitalInvestOpportunityPage'

    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = '/international/content/opportunities/ashton/'

    response = client.get(url)

    assert response.status_code == 404
