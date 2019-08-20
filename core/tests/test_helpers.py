import pytest

from directory_constants import expertise, sectors

from django.http import QueryDict
from django.urls import reverse

from core import helpers
from core.tests.helpers import create_response


@pytest.mark.parametrize('path,expect_code', (
    ('/', None),
    ('?language=pt', 'pt'),
    ('/industries?language=es', 'es'),
    ('/industries/?language=zh-hans', 'zh-hans'),
    ('/industries/aerospace?language=de', 'de'),
    ('/industries/automotive/?language=fr', 'fr'),
    ('?lang=fr', 'fr'),
    ('?language=de&lang=de', 'de'),
    ('?lang=pt&language=es', 'es')
))
def test_get_language_from_querystring(path, expect_code, rf):
    url = reverse('index')
    request = rf.get(url + path)
    language_code = helpers.get_language_from_querystring(request)
    assert language_code == expect_code


unslugify_slugs = [
    ('test-slug-one', 'Test slug one'),
    ('test-two', 'Test two'),
    ('slug', 'Slug'),
]


@pytest.mark.parametrize('slug,exp', unslugify_slugs)
def test_unslugify(slug, exp):
    assert helpers.unslugify(slug) == exp


def test_get_paginator_url():
    filters = QueryDict('')

    assert helpers.get_paginator_url(filters, 'opportunities') == (
        reverse('opportunities') + '?'
    )


def test_get_paginator_url_with_filters():
    filters = QueryDict('sector=Energy&sector=Aerospace&scale=Value+unknown')

    assert helpers.get_paginator_url(filters, 'opportunities') == (
        reverse('opportunities') + '?sector=Energy&sector=Aerospace&scale=Value+unknown'  # NOQA
    )


def test_get_paginator_url_with_spaces_filters():
    filters = QueryDict('sector=A+value+with+spaces+')

    assert helpers.get_paginator_url(filters, 'opportunities') == (
        reverse('opportunities') + '?sector=A+value+with+spaces+'
    )


def test_sort_opportunities_scale():

    opportunities = [
        {
            'scale_value': 100
        },
        {
            'scale_value': 3
        },
        {
            'scale_value': 30
        }
    ]

    sorting_chosen = helpers.SortFilter('Scale: High to Low')

    sorted_opps = helpers.sort_opportunities(opportunities, sorting_chosen)

    assert sorted_opps[0]['scale_value'] == 100
    assert sorted_opps[1]['scale_value'] == 30
    assert sorted_opps[2]['scale_value'] == 3


def test_sort_opportunities_name():

    opportunities = [
        {
            'title': 'Ashton Green'
        },
        {
            'title': 'Zoology'
        },
        {
            'title': 'Birmingham Curzon'
        },
    ]

    sorting_chosen = helpers.SortFilter('Project name: A to Z')

    sorted_opps = helpers.sort_opportunities(opportunities, sorting_chosen)

    assert sorted_opps[0]['title'] == 'Ashton Green'
    assert sorted_opps[1]['title'] == 'Birmingham Curzon'
    assert sorted_opps[2]['title'] == 'Zoology'


def test_filter_opportunities_scale():
    opportunities = [
        {
            'scale_value': 100
        },
        {
            'scale_value': 3
        },
        {
            'scale_value': 30
        },
        {
            'scale_value': 3000
        }
    ]

    filter_chosen = helpers.ScaleFilter('< £100m')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 2


def test_filter_opportunities_sub_sector():
    opportunities = [
        {
            'sub_sectors': ['Energy', 'Housing'],
        },
        {
            'sub_sectors': ['Mixed-use', 'Housing'],
        },
        {
            'sub_sectors': ['Energy', 'Mixed-use'],
        },
    ]

    filter_chosen = helpers.SubSectorFilter('Housing')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 2


def test_filter_opportunities_scale_value_unknown():
    opportunities = [
        {
            'scale_value': 100
        },
        {
            'scale_value': 1
        },
        {
            'scale_value': '0.00'
        },
        {
            'scale_value': 0.0
        },
        {
            'scale_value': '0'
        },
        {
            'scale_value': ''
        }
    ]

    filter_chosen = helpers.ScaleFilter('Value unknown')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 4


def test_filter_opportunities_scale_greater_than_1000():
    opportunities = [
        {
            'scale_value': 100
        },
        {
            'scale_value': 1
        },
        {
            'scale_value': 0
        },
        {
            'scale_value': 3000
        }
    ]

    filter_chosen = helpers.ScaleFilter('> £1bn')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 1


def test_filter_opportunities_region():
    opportunities = [
        {'related_region': {'title': 'Midlands'}},
        {'related_region': ''},
        {'related_region': {'title': 'Midlands'}},
        {'related_region': {'title': ''}},
    ]

    filter_chosen = helpers.RegionFilter('Midlands')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 2


def test_filter_opportunities_sector():
    opportunities = [
        {
            'related_sectors': [
                {'related_sector': {'heading': 'Aston Green'}},
                {'related_sector': {'heading': 'Birmingham Curzon'}},
            ],
        },
        {
            'related_sectors': [
                {'related_sector': {'heading': 'Aston Green'}},
            ],
        },
    ]

    filter_chosen = helpers.SectorFilter('Birmingham Curzon')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 1


def test_filter_opportunities_multiple_filters():
    opportunities = [
        {
            'title': 'this one',
            'related_sectors': [
                {'related_sector': ''},
                {'related_sector': {'heading': 'Birmingham Curzon'}},
                {'related_sector': {'heading': ''}},
            ],
            'scale_value': 0,
            'related_region': {'title': 'Midlands'},

        },
        {
            'title': 'not this one',
            'related_sectors': [
                {'related_sector': {'heading': 'Aston Green'}},
            ],
            'scale_value': 3000,
            'related_region': {'title': ''},
        },
    ]

    filtered_opps = helpers.filter_opportunities(opportunities, helpers.SectorFilter(
        'Birmingham Curzon'
    ))
    filtered_opps = helpers.filter_opportunities(filtered_opps, helpers.RegionFilter(
        'Midlands'
    ))
    filtered_opps = helpers.filter_opportunities(filtered_opps, helpers.ScaleFilter(
        'Value unknown'
    ))
    assert len(filtered_opps) == 1
    assert filtered_opps[0]['title'] == 'this one'


def test_company_parser_serialize_for_template(retrieve_profile_data):
    company = helpers.CompanyParser(retrieve_profile_data)

    assert company.serialize_for_template() == {
        'address': '123 Fake Street, Fakeville, London, E14 6XK',
        'address_line_1': '123 Fake Street',
        'address_line_2': 'Fakeville',
        'country': 'GB',
        'date_of_creation': '02 March 2015',
        'description': 'Ecommerce website',
        'email_address': 'test@example.com',
        'email_full_name': 'Jeremy',
        'employees': '501-1,000',
        'expertise_countries': '',
        'expertise_industries': '',
        'expertise_languages': '',
        'expertise_products_services': {},
        'expertise_regions': '',
        'facebook_url': 'http://www.facebook.com',
        'has_expertise': False,
        'keywords': 'word1, word2',
        'linkedin_url': 'http://www.linkedin.com',
        'locality': 'London',
        'logo': 'nice.jpg',
        'mobile_number': '07506043448',
        'modified': '2016-11-23T11:21:10.977518Z',
        'name': 'Great company',
        'number': '01234567',
        'po_box': 'abc',
        'postal_code': 'E14 6XK',
        'postal_full_name': 'Jeremy',
        'sectors': 'Security',
        'slug': 'great-company',
        'summary': 'this is a short summary',
        'supplier_case_studies': [],
        'twitter_url': 'http://www.twitter.com',
        'verified_with_code': True,
        'website': 'http://example.com',
        'company_type': 'COMPANIES_HOUSE',
        'is_published_investment_support_directory': True,
        'is_published_find_a_supplier': True,
        'is_in_companies_house': True
    }


def test_company_parser_serialize_for_template_empty():
    company = helpers.CompanyParser({})

    assert company.serialize_for_template() == {}


def test_get_results_from_search_response_xss(retrieve_profile_data):
    response = create_response({
        'hits': {
            'total': 1,
            'hits': [
                {
                    '_source': retrieve_profile_data,
                    'highlight': {
                        'description': [
                            '<a onmouseover=javascript:func()>stuff</a>',
                            'to the max <em>wolf</em>.'
                        ]
                    }

                }
            ]
        }
    })

    formatted = helpers.get_results_from_search_response(response)

    assert formatted['results'][0]['highlight'] == (
        '&lt;a onmouseover=javascript:func()&gt;stuff&lt;/a&gt;...to the max '
        '<em>wolf</em>.'
    )


def test_get_filters_labels():
    filters = {
        'expertise_languages': ['aa'],
        'q': 'foo',
        'page': 5,
        'expertise_regions': ['NORTH_EAST'],
        'expertise_products_services_financial': [expertise.FINANCIAL[1]],
        'industries': [sectors.AEROSPACE, sectors.ADVANCED_MANUFACTURING]
    }

    expected = [
        'Afar',
        'North East',
        'Insurance',
        'Aerospace',
        'Advanced manufacturing',
    ]

    assert helpers.get_filters_labels(filters) == expected


@pytest.fixture
def public_companies(retrieve_profile_data):
    return {
        'count': 100,
        'results': [retrieve_profile_data]
    }


@pytest.fixture
def public_companies_empty():
    return {
        'count': 0,
        'results': []
    }


def test_pair_sector_values_with_label():
    values = ['AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'AEROSPACE']
    expected = [
        {
            'label': 'Agriculture, horticulture and fisheries',
            'value': 'AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        },
        {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        }
    ]
    assert helpers.pair_sector_values_with_label(values) == expected


def test_pair_sector_values_with_label_contains_invalid():
    values = ['AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'AEROSPACE', 'DEFENCE']
    expected = [
        {
            'label': 'Agriculture, horticulture and fisheries',
            'value': 'AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        },
        {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        },
    ]

    assert helpers.pair_sector_values_with_label(values) == expected


def test_pair_sector_values_with_label_empty():
    for value in [None, []]:
        assert helpers.pair_sector_values_with_label(value) == []


def test_format_case_study():
    case_study = {
        'sector': 'AEROSPACE',
        'pk': '1',
        'slug': 'good-stuff',
    }
    expected = {
        'sector': {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        },
        'pk': '1',
        'slug': 'good-stuff',
        'case_study_url': '/international/trade/case-study/1/good-stuff/'
    }
    actual = helpers.format_case_study(case_study)
    assert actual == expected


def test_get_case_study_details_from_response(supplier_case_study_data):
    response = create_response(supplier_case_study_data)
    company = helpers.CompanyParser(supplier_case_study_data['company'])
    expected = {
        'description': 'Damn great',
        'year': '2000',
        'title': 'Two',
        'sector': {
            'value': 'SOFTWARE_AND_COMPUTER_SERVICES',
            'label': 'Software and computer services',
        },
        'testimonial': 'I found it most pleasing.',
        'keywords': 'great',
        'image_three': 'https://image_three.jpg',
        'pk': 2,
        'website': 'http://www.google.com',
        'image_two': 'https://image_two.jpg',
        'company': company.serialize_for_template(),
        'slug': 'two',
        'image_one': 'https://image_one.jpg',
        'video_one': 'https://video_one.wav',
    }
    assert helpers.get_case_study_details_from_response(response) == expected
