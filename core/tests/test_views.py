from unittest.mock import patch, call

import pytest

from django.urls import reverse

from conf.tests.test_urls import reload_urlconf
from core import constants
from core.forms import CapitalInvestContactForm
from core.tests.helpers import create_response, stub_page, dummy_page
from core.views import (
    MultilingualCMSPageFromPathView,
    CapitalInvestContactFormView,
    InternationalContactTriageView,
    WhyBuyFromUKFormView,
    WhyBuyFromUKFormViewSuccess
)

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


@pytest.fixture
def setup_in_uk_page():
    yield from stub_page({
        'page_type': 'InternationalGuideLandingPage',
        'guides': [],
    })


@pytest.fixture
def article_page():
    yield from stub_page({'page_type': 'InternationalArticlePage'})


@pytest.fixture
def home_page():
    yield from stub_page({'page_type': 'InternationalHomePage'})


@pytest.fixture
def international_capital_invest_page():
    yield from stub_page({
        'page_type': 'InternationalCapitalInvestLandingPage'
    })


@pytest.fixture
def about_uk_region_page():
    yield from stub_page({'page_type': 'AboutUkRegionPage'})


@pytest.fixture
def capital_invest_opportunity_page():
    yield from stub_page({
        'page_type': 'CapitalInvestOpportunityPage',
        'related_sectors': [
            {'related_sector': {'title': 'Test Sector'}}
        ]
    })


@pytest.fixture
def international_sub_sector_page():
    yield from stub_page({'page_type': 'InternationalSubSectorPage'})


@pytest.fixture
def capital_invest_contact_form_page():
    yield from stub_page({'page_type': 'CapitalInvestContactFormPage'})


@pytest.fixture
def capital_invest_contact_form_success_page():
    yield from stub_page({'page_type': 'CapitalInvestContactFormSuccessPage'})


@pytest.fixture
def about_uk_landing_page():
    yield from stub_page({'page_type': 'AboutUkLandingPage'})


def test_get_cms_page(rf, home_page):
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(request, path='/')

    assert response.context_data['page'] == home_page.return_value.json()


test_child_pages = [
    {
        'last_published_at': '2019-02-28T10:56:31.455848Z',
        'meta': {
            'slug': 'article-one',
            'languages': [['en-gb', 'English']],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article one teaser',
        'title': 'Article one'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-two',
            'languages': [['en-gb', 'English']],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article two teaser',
        'title': 'Article two'
    },
]

test_localised_child_pages = [
    {
        'last_published_at': '2019-02-28T10:56:31.455848Z',
        'meta': {
            'slug': 'article-one',
            'languages': [['en-gb', 'English']],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article one teaser',
        'title': 'Article one'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-two',
            'languages': [['en-gb', 'English']],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article two teaser',
        'title': 'Article two'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-three',
            'languages': [['en-gb', 'English']],
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
        'languages': [['en-gb', 'English']],
    },
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_sector_page_context_modifier_creates_filtered_cards_list(mock_get_page, rf):
    page = {
        'title': 'test',
        'landing_page_title': 'Industries',
        'page_type': 'InternationalTopicLandingPage',
        'child_pages': [
            {
                'meta': {
                    'languages': [
                        ['en-gb', 'English'],
                        ['fr-fr', 'Français']
                    ],
                },
                'full_path': '/international/content/investment/sectors/clean-growth/',
                'heading': 'Clean growth',
                'hero_image_thumbnail': {
                    'url': 'clean-growth.jpg',
                    'width': 640,
                    'height': 360,
                    'alt': 'Clean growth alt'
                },
                'sub_heading': 'The UK is leading',
            },
            {
                'meta': {
                    'languages': [
                        ['fr-fr', 'Français']
                    ],
                },
                'full_path': '/international/content/investment/sectors/some-other/',
                'title': 'Some other',
                'hero_image_thumbnail': None,
                'sub_heading': '',
            }
        ],
        'meta': {
            'slug': 'slug',
            'languages': [['en-gb', 'English']],
        },
    }
    mock_get_page.return_value = create_response(page)

    request = rf.get('/international/content/investment/sectors/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/investment/sectors/')

    assert len(response.context_data['cards_list']) == 1
    card_data = response.context_data['cards_list'][0]
    assert card_data['url'] == '/international/content/investment/sectors/clean-growth/'
    assert card_data['title'] == "Clean growth"
    assert card_data['image'] == "clean-growth.jpg"
    assert card_data['image_width'] == 640
    assert card_data['image_height'] == 360
    assert card_data['image_alt'] == "Clean growth alt"
    assert card_data['summary'] == "The UK is leading"


def test_cms_page_from_path_view(article_page, client, settings):
    response = client.get('/international/content/page/from/path/')

    assert response.status_code == 200

    article_page.assert_called_with(
        draft_token=None,
        language_code='en-gb',
        path='page/from/path',
        site_id=settings.DIRECTORY_CMS_SITE_ID,
    )


@pytest.mark.usefixtures('about_uk_region_page')
def test_about_uk_region_page_returns_404_when_feature_flag_off(
        client, settings
):
    settings.FEATURE_FLAGS['ABOUT_UK_REGION_PAGE_ON'] = False

    response = client.get('/international/content/about-uk/regions/region/')

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_about_uk_region_page_returns_200_when_feature_flag_on(
        mock_cms_response, rf, settings
):
    settings.FEATURE_FLAGS['ABOUT_UK_REGION_PAGE_ON'] = True

    page = {
        'title': 'Housing',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'housing'
        },
        'page_type': 'AboutUkRegionPage',
        'economics_stats': [],
        'location_stats': [],
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/content/about-uk/regions/region/'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request,
        path='/international/content/about-uk/regions/region/'
    )

    assert response.status_code == 200


@pytest.mark.usefixtures('international_sub_sector_page')
def test_capital_invest_sub_sector_page_returns_404_when_feature_flag_off(
        client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_SUB_SECTOR_PAGE_ON'] = False
    settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON'] = False
    reload_urlconf(settings)

    response = client.get(
        '/international/content/industries/energy/mixed-use/'
    )
    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_contact_form_page_returns_200_when_feature_flag_on(
        mock_cms_response, rf, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_CONTACT_FORM_PAGE_ON'] = True

    page = {
        'title': 'Contact',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'contact'
        },
        'page_type': 'CapitalInvestContactFormPage',
    }

    mock_cms_response.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get(
        '/international/content/capital-invest/contact/'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = CapitalInvestContactFormView.as_view()(
        request,
        path='/international/content/capital-invest/contact/'
    )

    assert 'fair-processing-notice-invest-in-great-britain' in response.context_data['privacy_url']

    assert response.status_code == 200


@pytest.mark.usefixtures('capital_invest_contact_form_page')
def test_capital_invest_contact_form_page_returns_404_when_feature_flag_off(
        client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_CONTACT_FORM_PAGE_ON'] = False

    response = client.get(
        '/international/content/investment/contact/'
    )
    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_contact_form_success_page_returns_200_when_feature_flag_on(
        mock_cms_response, rf, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_CONTACT_FORM_PAGE_ON'] = True

    page = {
        'title': 'Success',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'success'
        },
        'page_type': 'CapitalInvestContactFormSuccessPage',
    }

    mock_cms_response.return_value = create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get(
        '/international/content/investment/contact/success/'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request,
        path='/international/content/investment/contact/success/'
    )

    assert response.status_code == 200


@pytest.mark.usefixtures('capital_invest_contact_form_success_page')
def test_capital_invest_contact_form_success_page_returns_404_when_feature_flag_off(
        client, settings
):
    settings.FEATURE_FLAGS['CAPITAL_INVEST_CONTACT_FORM_PAGE_ON'] = False

    response = client.get(
        '/international/content/investment/contact/success/'
    )
    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_international_contact_form(mock_cms_response, client, settings):
    settings.FEATURE_FLAGS['INTERNATIONAL_TRIAGE_ON'] = False
    reload_urlconf(settings)

    mock_cms_response.return_value = create_response(dummy_page)

    url = reverse('contact-page-international')
    response = client.get(url)

    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_show_featured_cards_section_on_invest_home_page(
        mock_cms_response, rf
):
    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'InvestInternationalHomePage',
        'high_potential_opportunities': [],
        'featured_cards': [
            {
                'title': 'Get started in the UK',
                'image': {
                    'url': 'https://directory-cms-public.s3.amazonaws.com'
                           '/images/Get_started_in_the_UK.2e16d0ba.'
                           'fill-640x360_i3FI8OQ.jpg',
                    'width': 640,
                    'height': 360
                },
                'summary': 'A summary',
            },
            {
                'title': 'Get started in the UK',
                'image': {
                    'url': 'https://directory-cms-public.s3.amazonaws.com'
                           '/images/Get_started_in_the_UK.2e16d0ba.'
                           'fill-640x360_i3FI8OQ.jpg',
                    'width': 640,
                    'height': 360
                },
                'summary': 'A summary',
                'cta_link': 'www.google.com'
            },
            {
                'title': 'Get started in the UK',
                'image': {
                    'url': 'https://directory-cms-public.s3.amazonaws.com'
                           '/images/Get_started_in_the_UK.2e16d0ba.'
                           'fill-640x360_i3FI8OQ.jpg',
                    'width': 640,
                    'height': 360
                },
                'summary': 'A summary',
            },
        ],
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/content/midlands/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/midlands/')

    assert response.context_data['show_featured_cards'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_show_featured_cards_section_doesnt_show_when_missing_some_on_invest_home_page(
        mock_cms_response, rf
):
    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'InvestInternationalHomePage',
        'high_potential_opportunities': [],
        'featured_cards': [
            {
                'title': '',
                'image': {},
                'summary': 'A summary',
            },
            {
                'title': 'Get started in the UK',
                'image': {},
                'summary': 'A summary',
                'cta_link': 'www.google.com'
            },
            {
                'title': 'Get started in the UK',
                'image': {},
                'summary': '',
            },
        ],
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/content/midlands/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/midlands/')

    assert response.context_data['show_featured_cards'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_show_featured_cards_section_doesnt_show_when_missing_on_invest_home_page(
        mock_cms_response, rf
):
    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['de', 'Deutsch'],
            ]
        },
        'page_type': 'InvestInternationalHomePage',
        'high_potential_opportunities': [],
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/content/midlands/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/midlands/')

    assert response.context_data['show_featured_cards'] is False


@pytest.fixture
def capital_invest_contact_form_data(captcha_stub):
    return {
        'given_name': 'Steve',
        'family_name': 'Rogers',
        'email_address': 'captain_america@avengers.com',
        'phone_number': '01234 567891',
        'country': 'FR',
        'message': 'foobar',
        'email_contact_consent': True,
        'telephone_contact_consent': True,
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True
    }


@patch.object(CapitalInvestContactFormView.form_class, 'save')
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_capital_invest_contact_form_success(
        mock_lookup_by_path, mock_save, client, capital_invest_contact_form_data
):
    mock_lookup_by_path.return_value = create_response(
        status_code=200,
        json_payload={
            'title': 'Contact Form',
            'meta': {
                'languages': [
                    ['en-gb', 'English']
                ],
                'slug': 'contact',
            },
            'page_type': 'CapitalInvestContactFormPage'
        }
    )
    mock_save.return_value = create_response(status_code=200)

    url = reverse('investment-contact')
    response = client.post(url, capital_invest_contact_form_data)

    assert response.status_code == 302
    assert response.url == '/international/content/investment/contact/success'


@pytest.mark.parametrize('page_type,url', [
    ('AboutUkRegionPage', '/international/content/about-uk/regions/scotland'),
    ('AboutUkRegionListingPage', '/international/content/about-uk/regions/')
])
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_getting_keyed_region_data_on_region_listing_page(mock_cms_response, rf, page_type, url):
    page = {  # NOQA
        'title': 'Regions',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ]
        },
        'page_type': page_type,
        'mapped_regions': [
            {
                'region': {
                    'meta': {
                        'slug': 'scotland',
                        'languages': [['en-gb', 'English']]
                    },
                    'title': 'Scotland',
                    'full_path': '/international/content/about-uk/regions/scotland/',
                },
                'text': 'Lorem ipsum'
            },
            {
                'region': {
                    'meta': {
                        'slug': 'northern-ireland',
                        'languages': [['en-gb', 'English']]
                    },
                    'title': 'The Northern Ireland',
                    'full_path': '/international/content/about-uk/regions/northern-ireland/',
                },
                'text': 'Lorem ipsum'
            },
            {
                'region': {
                    'meta': {
                        'slug': 'north-of-england',
                        'languages': [['en-gb', 'English']]
                    },
                    'title': 'North England',
                    'full_path': '/international/content/about-uk/regions/north-england/',
                },
                'text': 'Lorem ipsum'
            },
        ],
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(url)
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(request, path=url)

    assert len(response.context_data['regions']) == 3
    assert response.context_data['regions']['scotland'][
               'full_path'] == '/international/content/about-uk/regions/scotland/'
    assert response.context_data['regions']['north_of_england'][
               'full_path'] == '/international/content/about-uk/regions/north-england/'
    assert response.context_data['regions']['northern_ireland'][
               'full_path'] == '/international/content/about-uk/regions/northern-ireland/'


@pytest.mark.parametrize('page_type,url', [
    ('AboutUkRegionPage', '/international/content/about-uk/regions/scotland'),
    ('AboutUkRegionListingPage', '/international/content/about-uk/regions/')
])
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_region_page_context_decorator_adds_cards_list(mock_cms_response, rf, page_type, url):
    page = {  # NOQA
        'title': 'Regions',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ]
        },
        'page_type': page_type,
        'mapped_regions': [
            {
                'region': {
                    'meta': {
                        'slug': 'scotland',
                        'languages': [['en-gb', 'English']]
                    },
                    'title': 'Scotland',
                    'full_path': '/international/content/about-uk/regions/scotland/',
                    'hero_image_thumbnail': {
                        'url': 'scotland.jpg',
                        'width': 640,
                        'height': 360,
                        'alt': 'Scotland scene'
                    }
                },
                'text': 'Lorem ipsum Scotland'
            },
            {
                'region': {
                    'meta': {
                        'slug': 'northern-ireland',
                        'languages': [['en-gb', 'English']]
                    },
                    'title': 'The Northern Ireland',
                    'full_path': '/international/content/about-uk/regions/northern-ireland/',
                    'hero_image_thumbnail': None
                },
                'text': 'Lorem ipsum'
            },
            {
                'region': {
                    'meta': {
                        'slug': 'north-of-england',
                        'languages': [['en-gb', 'English']]
                    },
                    'title': 'North England',
                    'full_path': '/international/content/about-uk/regions/north-england/',
                    'hero_image_thumbnail': {
                        'url': 'north-england.jpg',
                        'width': 640,
                        'height': 360,
                        'alt': 'North of England scene'
                    }
                },
                'text': 'Lorem ipsum'
            },
        ],
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(url)
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(request, path=url)

    assert len(response.context_data['cards_list']) == 3
    card = response.context_data['cards_list'][0]
    assert card['title'] == 'Scotland'
    assert card['summary'] == 'Lorem ipsum Scotland'
    assert card['image'] == 'scotland.jpg'
    assert card['image_alt'] == 'Scotland scene'
    assert card['image_width'] == 640
    assert card['image_height'] == 360

    assert 'image' not in response.context_data['cards_list'][1]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_atlas_opportunity_page_sectors_label(mock_cms_response, rf):
    page = {  # NOQA
        'title': 'Test',
        'meta': {'languages': [['en-gb', 'English']]},
        'page_type': 'InvestmentOpportunityPage',
        'related_sectors': [
            {'related_sector': {'title': 'Housing'}},
            {'related_sector': {'title': 'Aerospace'}}
        ],
        'sub_sectors': ['Green housing', 'Urban', 'Renting']
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/content/investment/opportunities/test/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/investment/opportunities/test/')

    # we dont have sector, sub-sector relation in database hence putting everything in bracket rather showing
    # indiviual sector with subsector
    assert response.context_data['sectors_label'] == '(Housing, Aerospace, Green housing, Urban, Renting)'


@pytest.mark.skip("No longer relevant - redirects stop this being accessed. Retaining test for awareness")
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_expand_path_exists(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    page = {
        'title': 'Expand to the UK',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'expand'
        },
        'page_type': 'InvestInternationalHomePage',
    }

    def side_effect(*args, **kwargs):
        if kwargs['path'] == 'invest':
            return create_response(status_code=404)
        if kwargs['path'] == 'expand':
            return create_response(json_payload=page, status_code=200)
        return create_response(status_code=500)

    mock_get_page.side_effect = side_effect

    url = reverse('invest-home')
    response = client.get(url)

    assert mock_get_page.call_count == 2
    assert mock_get_page.mock_calls[1] == call(
        draft_token=None,
        language_code='en-gb',
        path='expand',
        site_id=2
    )
    assert response.status_code == 200


@patch.object(CapitalInvestContactFormView.form_class, 'save')
def test_capital_invest_contact_serialized_data(mock_save, capital_invest_contact_form_data):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data
    )

    assert form.is_valid()

    mock_save.return_value = create_response(status_code=200)

    assert form.serialized_data == {
        'given_name': capital_invest_contact_form_data['given_name'],
        'family_name': capital_invest_contact_form_data['family_name'],
        'email_address': capital_invest_contact_form_data['email_address'],
        'phone_number': capital_invest_contact_form_data['phone_number'],
        'country': capital_invest_contact_form_data['country'],
        'message': capital_invest_contact_form_data['message'],
        'email_contact_consent': capital_invest_contact_form_data['email_contact_consent'],
        'telephone_contact_consent': capital_invest_contact_form_data['telephone_contact_consent'],
    }


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_industries_about_uk_path_exists(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON'] = False
    reload_urlconf(settings)

    page = {
        'title': 'Industries',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ],
            'slug': 'industries'
        },
        'page_type': 'InternationalTopicLandingPage',
        'landing_page_title': 'title',
        'child_pages': [
            {
                'meta': {
                    'slug': 'page',
                    'languages': [['en-gb', 'English']],
                },
                'heading': 'title',
                'sub_heading': 'heading',
                'full_path': '/some-url/',
                'hero_image_thumbnail': None
            }
        ]
    }

    def side_effect(*args, **kwargs):
        if kwargs['path'] == 'industries':
            return create_response(status_code=404)
        if kwargs['path'] == 'about-uk/industries':
            return create_response(json_payload=page, status_code=200)
        return create_response(status_code=500)

    mock_get_page.side_effect = side_effect

    response = client.get('/international/content/industries/')

    assert mock_get_page.call_count == 2
    assert mock_get_page.mock_calls[1] == call(
        draft_token=None,
        language_code='en-gb',
        path='about-uk/industries',
        site_id=2
    )
    assert response.status_code == 200


def test_business_environment_form_view(client):
    response = client.get(reverse('business-environment-guide-form'))
    assert 'privacy-notice-uk-investment-prospectus' in response.context_data['privacy_url']
    assert response.status_code == 200


def test_business_environment_form_success_view(client):
    response = client.get(reverse('business-environment-guide-form-success'))
    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_about_uk_breadcrumbs_article_page_feature_on(
        mock_cms_response, rf, settings
):
    settings.FEATURE_FLAGS['ABOUT_UK_LANDING_PAGE_ON'] = True

    page = {
        'title': 'Tax and incentives',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ]
        },
        'page_type': 'InternationalArticlePage',
        'tree_based_breadcrumbs': [
            {
                'title': 'About the UK',
                'url': 'http://international.trade.great:8012/international/content/about-uk/'
            },
            {
                'title': 'Why choose the UK',
                'url': 'http://international.trade.great:8012/international/content/about-uk/why-choose-uk/'
            }
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/content/about-uk/why-choose-uk/tax/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/about-uk/why-choose-uk/tax/')

    assert len(response.context_data['page']['tree_based_breadcrumbs']) == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_about_uk_breadcrumbs_article_page_feature_off(
        mock_cms_response, rf, settings
):
    settings.FEATURE_FLAGS['ABOUT_UK_LANDING_PAGE_ON'] = False

    page = {
        'title': 'Tax and incentives',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ]
        },
        'page_type': 'InternationalArticlePage',
        'tree_based_breadcrumbs': [
            {
                'title': 'About the UK',
                'url': 'http://international.trade.great:8012/international/content/about-uk/'
            },
            {
                'title': 'Why choose the UK',
                'url': 'http://international.trade.great:8012/international/content/about-uk/why-choose-uk/'
            }
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/content/about-uk/why-choose-uk/tax/')
    request.LANGUAGE_CODE = 'en-gb'
    response = MultilingualCMSPageFromPathView.as_view()(
        request, path='/international/content/about-uk/why-choose-uk/tax/')

    assert len(response.context_data['page']['tree_based_breadcrumbs']) == 1
    assert response.context_data['page']['tree_based_breadcrumbs'][0]['title'] == 'Why choose the UK'


@pytest.mark.parametrize(
    'choice_contact_url',
    [constants.INVEST_CONTACT_URL, constants.CAPITAL_INVEST_CONTACT_URL, constants.EXPORTING_TO_UK_CONTACT_URL,
     constants.BUYING_CONTACT_URL, constants.EUEXIT_CONTACT_URL, constants.OTHER_CONTACT_URL]
)
def test_international_contact_triage_redirects(
        choice_contact_url, client, feature_flags
):
    feature_flags['INTERNATIONAL_TRIAGE_ON'] = True
    feature_flags['EXPORTING_TO_UK_ON'] = True
    feature_flags['CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'] = True

    response = client.post('/international/contact/', {'choice': choice_contact_url})
    assert response.status_code == 302
    assert response.url == choice_contact_url


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_international_contact_triage_view(
        mock_cms_response, rf
):
    page = {
        'title': 'Midlands',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ]
        }
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/contact/')
    request.LANGUAGE_CODE = 'en-gb'
    response = InternationalContactTriageView.as_view()(
        request, path='/international/contact/')

    assert 'domestic_contact_home' in response.context_data


@pytest.fixture
def why_buy_from_uk_form_data(captcha_stub):
    return {
        'given_name': 'Test',
        'family_name': 'User',
        'email_address': 'me@here.com',
        'company_name': 'Company LTD',
        'job_title': 'Director',
        'phone_number': '07777777777',
        'market': 'FR',
        'industry': 'ADVANCED_MANUFACTURING',
        'procuring_products': 'yes',
        'contact_email': False,
        'contact_phone': True,
        'city': 'London',
        'g-recaptcha-response': captcha_stub,
    }


def test_why_buy_from_uk_form_data_view(client):
    response = client.get(reverse('why-buy-from-uk-form'))
    assert response.status_code == 200


@patch.object(WhyBuyFromUKFormView.form_class, 'save')
def test_why_buy_from_uk_submission(mock_save, why_buy_from_uk_form_data, client):
    mock_save.return_value = create_response(status_code=200)

    response = client.post(reverse('why-buy-from-uk-form'), why_buy_from_uk_form_data)

    assert mock_save.call_count == 2
    assert response.status_code == 302
    assert response.url == reverse('why-buy-from-uk-form-success')


def test_why_buy_from_uk_form_success_view(client):
    response = client.get(reverse('why-buy-from-uk-form'))
    assert response.status_code == 200


def test_why_buy_from_uk_context(rf, client):
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'
    response = WhyBuyFromUKFormView.as_view()(
        request, path='/international/content/trade/how-we-help-you-buy/why-buy-from-the-uk/')
    assert '/international/trade/' in response.context_data['international_trade_home']
    assert (
            '/international/content/trade/how-we-help-you-buy/'
            in response.context_data['international_trade_how_we_help']
    )
    assert 'privacy-notice-5-reasons-buy-uk' in response.context_data['privacy_url']


def test_why_buy_from_uk_success_context(rf, client):
    request = rf.get('/')
    response = WhyBuyFromUKFormViewSuccess.as_view()(
        request, path='/international/content/trade/how-we-help-you-buy/why-buy-from-the-uk/success/')
    assert '/international/trade/' in response.context_data['international_trade_home']
    assert (
            '/international/content/trade/how-we-help-you-buy/'
            in response.context_data['international_trade_how_we_help']
    )
