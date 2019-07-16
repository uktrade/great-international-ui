from unittest.mock import patch

from bs4 import BeautifulSoup
from directory_constants import urls
import pytest

from django.urls import reverse

from core import helpers
from core.tests.helpers import create_response
from core.views import CMSPageFromPathView, cms_api_client, \
    OpportunitySearchView

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
    'display_title': 'Title',
    'breadcrumbs_label': 'Title',
    'meta': {
        'languages': [
            ['en-gb', 'English'],
            ['fr', 'Français'],
            ['de', 'Deutsch'],
        ]
    },
    'page_type': 'InternationalHomePage',
}


def stub_page(page):
    value = create_response(json_payload={**dummy_page, **page})
    stub = patch.object(cms_api_client, 'lookup_by_path', return_value=value)
    yield stub.start()
    stub.stop()


@pytest.fixture
def setup_in_uk_page():
    yield from stub_page({
        'page_type': 'InternationalGuideLandingPage',
        'guides': [],
    })


@pytest.fixture
def how_to_do_business_uk_page():
    yield from stub_page({'page_type': 'InternationalCuratedTopicLandingPage'})


@pytest.fixture
def home_page():
    yield from stub_page({'page_type': 'InternationalHomePage'})


@pytest.fixture
def international_capital_invest_page():
    yield from stub_page({
        'page_type': 'InternationalCapitalInvestLandingPage'
    })


@pytest.fixture
def capital_invest_page():
    yield from stub_page({'page_type': 'CapitalInvestRegionPage'})


@pytest.fixture
def capital_invest_opportunity_page():
    yield from stub_page({'page_type': 'CapitalInvestOpportunityPage'})


@pytest.fixture
def international_sub_sector_page():
    yield from stub_page({'page_type': 'InternationalSubSectorPage'})


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


@pytest.mark.usefixtures('home_page')
def test_cms_language_switcher_active_language_available(rf):
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = CMSPageFromPathView.as_view()(request, path='/international/')

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True


def test_get_cms_page(rf, home_page):
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(request, path='/')

    assert response.context_data['page'] == home_page.return_value.json()


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_article_detail_page_social_share_links(
    mock_get_page, client, settings
):

    test_article_page = {
        'title': 'Test article',
        'display_title': 'Test article',
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
    assert response.template_name == [
        'core/uk_setup_guide/article_detail.html'
    ]

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
        'display_title': 'Test article',
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
    assert response.template_name == [
        'core/uk_setup_guide/article_detail.html'
    ]

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
        'related_opportunities': [
            {
                'title': 'Sector',
                'hero_image': {'url': 'article_list.png'},
                'sub_sectors': ['energy', 'housing-led'],
                'scale': 'scale',
            },
        ],
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
def test_industry_page_context_modifier_renames_heading(mock_get_page, client):
    page = {
        'title': 'test',
        'landing_page_title': 'Industries',
        'page_type': 'InternationalTopicLandingPage',
        'child_pages': [
            {
                'heading': 'heading',
                'meta': {
                    'languages': [('en-gb', 'English')],
                },
            }
        ],
        'statistics': [],
        'section_three_subsections': [],
        'meta': {
            'slug': 'slug',
            'languages': [('en-gb', 'English')],
        },
    }
    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    url = reverse('industries')
    response = client.get(url)

    child_page = response.context_data['page']['child_pages'][0]
    assert child_page['landing_page_title'] == 'heading'


@pytest.mark.usefixtures('how_to_do_business_uk_page')
def test_how_to_do_business_feature_off(client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = False

    response = client.get(reverse('how-to-do-business-with-the-uk'))

    assert response.status_code == 404


@pytest.mark.usefixtures('how_to_do_business_uk_page')
def test_how_to_do_business_feature_on(client, settings):
    settings.FEATURE_FLAGS['HOW_TO_DO_BUSINESS_ON'] = True

    response = client.get(reverse('how-to-do-business-with-the-uk'))

    assert response.status_code == 200


def test_cms_page_from_path_view(how_to_do_business_uk_page, client, settings):

    response = client.get('/international/content/page/from/path/')

    assert response.status_code == 200

    how_to_do_business_uk_page.assert_called_with(
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

    request = rf.get('/international/content/midlands/')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/midlands/')

    assert response.context_data['num_of_economics_statistics'] == 2
    assert response.context_data['num_of_location_statistics'] == 1


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


@pytest.mark.usefixtures('international_capital_invest_page')
def test_capital_invest_landing_page_returns_404_when_feature_flag_off(
    client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_LANDING_PAGE_ON'] = False

    response = client.get('/international/content/capital-invest/')

    assert response.status_code == 404


@pytest.mark.usefixtures('international_capital_invest_page')
def test_capital_invest_landing_page_returns_200_when_feature_flag_on(
    client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_LANDING_PAGE_ON'] = True

    response = client.get('/international/content/capital-invest/')

    assert response.status_code == 200


@pytest.mark.usefixtures('capital_invest_page')
def test_capital_invest_region_page_returns_404_when_feature_flag_off(
    client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_REGION_PAGE_ON'] = False

    response = client.get('/international/content/midlands/')

    assert response.status_code == 404


@pytest.mark.usefixtures('capital_invest_opportunity_page')
def test_capital_invest_opportunity_page_returns_404_when_feature_flag_off(
    client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_OPPORTUNITY_PAGE_ON'] = False

    response = client.get('/international/content/opportunities/ashton/')

    assert response.status_code == 404


@pytest.mark.usefixtures('capital_invest_opportunity_page')
def test_capital_invest_opportunity_page_returns_200_when_feature_flag_on(
    client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_OPPORTUNITY_PAGE_ON'] = True

    response = client.get('/international/content/opportunities/ashton/')

    assert response.status_code == 200


@pytest.mark.usefixtures('international_sub_sector_page')
def test_capital_invest_sub_sector_page_returns_404_when_feature_flag_off(
    client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_SUB_SECTOR_PAGE_ON'] = False

    response = client.get(
        '/international/content/industries/energy/mixed-use/'
    )
    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_sub_sector_page_returns_200_when_feature_flag_on(
    mock_cms_response, rf, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_SUB_SECTOR_PAGE_ON'] = True

    page = {
        'title': 'Housing',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'housing'
        },
        'page_type': 'InternationalSubSectorPage',
        'statistics': [],
        'section_three_subsections': [],
        'related_opportunities': []
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get(
        '/international/content/industries/energy/housing'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request,
        path='/international/content/industries/energy/housing'
    )

    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_international_contact_form(mock_cms_response, client):
    mock_cms_response.return_value = create_response(
        status_code=200,
        json_payload=dummy_page
    )

    url = reverse('contact-page-international')
    response = client.get(url)

    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_region_sector_scale_filter_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'related_region': {
                    'title': 'Midlands'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 2',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'Midlands'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Automotive'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 3',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '0.00',
                'related_region': {
                    'title': 'South of Engalnd'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Automotive'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/?sector=Aerospace&scale=Value+unknown&region=Midlands')   # NOQA
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request, path='/international/content/opportunities/?sector=Aerospace&scale=Value+unknown&region=Midlands')  # NOQA

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'  # NOQA


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_num_of_opportunities_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 2',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'Midlands'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/?sector=Aerospace')
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request, path='/international/content/opportunities?sector=Aerospace')

    assert response.context_data['num_of_opportunities'] == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_filters_chosen_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/?scale=<+£100m')
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request, path='/international/content/opportunities/?scale=<+£100m')

    assert len(response.context_data['filters']) == 1
    assert '< £100m' in response.context_data['filters']


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_sorting_filters_chosen_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/?sort_by=Scale%3A+Low+to+High&region=Midlands')  # NOQA
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request, path='/international/content/opportunities/?sort_by=Scale%3A+Low+to+High&regionMidlands')  # NOQA

    assert response.context_data['sorting_chosen'] == 'Scale: Low to High'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_sub_sector_filters_chosen_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/?sub_sector=housing')  # NOQA
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request, path='/international/content/opportunities/?sub_sector=housing')  # NOQA

    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'  # NOQA
    assert len(response.context_data['pagination'].object_list) == 1


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_goes_to_page_one_if_page_num_too_big_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get(
        '/international/content/opportunities/?page=10'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request,
        path='/international/content/opportunities/'
             '?page=10'
    )

    assert response.url == '/international/content/opportunities/?&page=1'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_goes_to_page_one_if_page_num_not_a_num_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get(
        '/international/content/opportunities/?page=qq'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request,
        path='/international/content/opportunities/?page=qq'
    )

    assert response.url == '/international/content/opportunities/?&page=1'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_sub_sectors_being_shown_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['housing'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'South of England'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy'],
                'scale_value': '1000.00',
                'related_region': {
                    'title': 'Midlands'
                },
                'related_sectors': [
                    {
                        'related_sector': {
                            'title': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request_two_sub_sectors = rf.get(
        '/international/content/opportunities/?sub_sector=housing&sub_sector=energy')  # NOQA
    request_two_sub_sectors.LANGUAGE_CODE = 'en-gb'
    response_two_sub_sectors = OpportunitySearchView.as_view()(
        request_two_sub_sectors,
        path='/international/content/opportunities/?sub_sector=housing&sub_sector=energy')  # NOQA

    assert len(response_two_sub_sectors.context_data['sub_sectors']) == 2

    request_one_sub_sector = rf.get('/international/content/opportunities/?sub_sector=housing')  # NOQA
    request_one_sub_sector.LANGUAGE_CODE = 'en-gb'
    response_one_sub_sector = OpportunitySearchView.as_view()(
        request_one_sub_sector, path='/international/content/opportunities/?sub_sector=housing')  # NOQA

    assert len(response_one_sub_sector.context_data['sub_sectors']) == 1

    request_two_with_only_one_in_results = rf.get('/international/content/opportunities/?sub_sector=housing&sub_sector=energy&sector=Midlands')  # NOQA
    request_two_with_only_one_in_results.LANGUAGE_CODE = 'en-gb'
    response_two_with_only_one_in_results = OpportunitySearchView.as_view()(
        request_two_with_only_one_in_results, path='/international/content/opportunities/?sub_sector=housing&sub_sector=energy&sector=Midlands')  # NOQA

    assert len(
        response_two_with_only_one_in_results.context_data['sub_sectors']
    ) == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_random_three_opportunities_for_sector_page(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'sector'
        },
        'page_type': 'InternationalSectorPage',
        'related_opportunities': [
            {
                'title': 'Aerospace',
                'hero_image': {'url': 'article_list.png'},
                'sector': 'Sector1',
                'scale': 'scale',
            },
            {
                'title': 'Aerospace',
                'hero_image': {'url': 'article_list.png'},
                'sector': 'Sector2',
                'scale': 'scale',
            },
            {
                'title': 'Aerospace',
                'hero_image': {'url': 'article_list.png'},
                'sector': 'Sector3',
                'scale': 'scale',
            },
            {
                'title': 'Aerospace',
                'hero_image': {'url': 'article_list.png'},
                'sector': 'Sector4',
                'scale': 'scale',
            },
        ],
        'statistics': [],
        'section_three_subsections': []
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/industries/sector')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/industries/sector')

    assert len(response.context_data['random_opportunities']) == 3


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_random_three_opportunities_for_sector_page_null_case(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'sector'
        },
        'page_type': 'InternationalSectorPage',
        'statistics': [],
        'section_three_subsections': []
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/industries/sector')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/industries/sector')

    assert len(response.context_data['random_opportunities']) == 0


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_random_three_opportunities_for_sub_sector_page_null_case(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'sector'
        },
        'page_type': 'InternationalSubSectorPage',
        'statistics': [],
        'section_three_subsections': []
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/industries/sector/sub_sector')
    request.LANGUAGE_CODE = 'en-gb'
    response = CMSPageFromPathView.as_view()(
        request, path='/international/content/industries/sector/sub_sector')

    assert len(response.context_data['random_opportunities']) == 0


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_when_no_opportunity_list_in_page_for_opportunity_search(
        mock_cms_response, rf):

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ],
            'slug': 'opportunities'
        },
        'page_type': 'CapitalInvestOpportunityListingPage',
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/international/content/opportunities/')  # NOQA
    request.LANGUAGE_CODE = 'en-gb'
    response = OpportunitySearchView.as_view()(
        request, path='/international/content/opportunities/')  # NOQA

    assert response.context_data['num_of_opportunities'] == 0
