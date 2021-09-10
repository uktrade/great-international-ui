import pytest

from directory_constants import expertise, sectors

from django.http import QueryDict
from django.urls import reverse

from core import helpers
from core.helpers import get_map_labels_with_vertical_positions, get_header_config
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

    assert helpers.get_paginator_url(filters, 'atlas-opportunities') == (
            reverse('atlas-opportunities') + '?'
    )


def test_get_paginator_url_with_filters():
    filters = QueryDict('sector=Energy&sector=Aerospace&scale=Value+unknown')

    assert helpers.get_paginator_url(filters, 'atlas-opportunities') == (
            reverse('atlas-opportunities') + '?sector=Energy&sector=Aerospace&scale=Value+unknown'  # NOQA
    )


def test_get_paginator_url_with_spaces_filters():
    filters = QueryDict('sector=A+value+with+spaces+')

    assert helpers.get_paginator_url(filters, 'atlas-opportunities') == (
            reverse('atlas-opportunities') + '?sector=A+value+with+spaces+'
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


def test_filter_opportunities_region__single():
    opportunities = [
        {'slug': 'one', 'related_regions': [{'title': 'Midlands'}]},
        {'slug': 'two', 'related_regions': []},
        {'slug': 'three', 'related_regions': [{'title': 'Midlands'}]},
        {'slug': 'four', 'related_regions': [{'title': ''}]},
    ]

    filter_chosen = helpers.MultipleRegionsFilter('Midlands')

    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 2
    assert sorted([x['slug'] for x in filtered_opps]) == ['one', 'three']


def test_filter_opportunities_region__multiple():
    opportunities = [
        {'slug': 'one', 'related_regions': [{'title': 'Midlands'}]},
        {'slug': 'two', 'related_regions': []},
        {'slug': 'three', 'related_regions': [{'title': 'Midlands'}, {'title': 'Wales'}]},
        {'slug': 'four', 'related_regions': [{'title': 'Midlands'}]},
        {'slug': 'five', 'related_regions': [{'title': 'Wales'}]},
        {'slug': 'six', 'related_regions': [{'title': 'Midlands'}]},
        {'slug': 'seven', 'related_regions': [{'title': ''}]},
    ]

    filter_chosen = helpers.MultipleRegionsFilter('Midlands')
    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 4

    assert sorted([x['slug'] for x in filtered_opps]) == ['four', 'one', 'six', 'three']

    filter_chosen = helpers.MultipleRegionsFilter('Wales')
    filtered_opps = helpers.filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 2
    assert sorted([x['slug'] for x in filtered_opps]) == ['five', 'three']


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
            'related_regions': [{'title': 'Midlands'}],

        },
        {
            'title': 'not this one',
            'related_sectors': [
                {'related_sector': {'heading': 'Aston Green'}},
            ],
            'scale_value': 3000,
            'related_regions': [{'title': ''}],
        },
    ]

    filtered_opps = helpers.filter_opportunities(opportunities, helpers.SectorFilter(
        'Birmingham Curzon'
    ))
    filtered_opps = helpers.filter_opportunities(filtered_opps, helpers.MultipleRegionsFilter(
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
        'industries': [sectors.AEROSPACE, sectors.ADVANCED_MANUFACTURING],
        'expertise_products_services_human_resources': [
            'Employment and talent research'
        ]
    }

    expected = [
        'Afar',
        'North East',
        'Insurance',
        'Aerospace',
        'Advanced manufacturing',
        'Employment and talent research',
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


def test_get_map_labels_with_vertical_positions_one_word():
    words_with_coordinates = get_map_labels_with_vertical_positions(['midlands'], 100, 100)

    assert len(words_with_coordinates) == 1
    assert words_with_coordinates[0]['x'] == '100'
    assert words_with_coordinates[0]['y'] == '100.0'


def test_get_map_labels_with_vertical_positions_two_words():
    words_with_coordinates = get_map_labels_with_vertical_positions(['south', 'england'], 100, 100)

    assert len(words_with_coordinates) == 2
    assert words_with_coordinates[0]['title'] == 'south'
    assert words_with_coordinates[0]['x'] == '100'
    assert words_with_coordinates[0]['y'] == '87.5'

    assert words_with_coordinates[1]['title'] == 'england'
    assert words_with_coordinates[1]['x'] == '100'
    assert words_with_coordinates[1]['y'] == '112.5'


def test_get_map_labels_with_vertical_positions_three_words():
    words_with_coordinates = get_map_labels_with_vertical_positions(['south', 'of', 'england'], 100, 100)

    assert len(words_with_coordinates) == 3
    assert words_with_coordinates[0]['title'] == 'south'
    assert words_with_coordinates[0]['x'] == '100'
    assert words_with_coordinates[0]['y'] == '75.0'

    assert words_with_coordinates[1]['title'] == 'of'
    assert words_with_coordinates[1]['x'] == '100'
    assert words_with_coordinates[1]['y'] == '100.0'

    assert words_with_coordinates[2]['title'] == 'england'
    assert words_with_coordinates[2]['x'] == '100'
    assert words_with_coordinates[2]['y'] == '125.0'


def test_get_map_labels_with_vertical_positions_four_words():
    words_with_coordinates = get_map_labels_with_vertical_positions(['the', 'south', 'of', 'england'], 100, 100)

    assert len(words_with_coordinates) == 4
    assert words_with_coordinates[0]['title'] == 'the'
    assert words_with_coordinates[0]['x'] == '100'
    assert words_with_coordinates[0]['y'] == '62.5'

    assert words_with_coordinates[1]['title'] == 'south'
    assert words_with_coordinates[1]['x'] == '100'
    assert words_with_coordinates[1]['y'] == '87.5'

    assert words_with_coordinates[2]['title'] == 'of'
    assert words_with_coordinates[2]['x'] == '100'
    assert words_with_coordinates[2]['y'] == '112.5'

    assert words_with_coordinates[3]['title'] == 'england'
    assert words_with_coordinates[3]['x'] == '100'
    assert words_with_coordinates[3]['y'] == '137.5'


@pytest.mark.parametrize('path,expected_section_name,expected_sub_section_name', [
    ('', '', ''),
    ('about-uk', 'about-uk', 'overview-about-uk'),
    ('about-uk/regions', 'about-uk', 'regions'),
    ('about-uk/regions/wales', 'about-uk', 'regions'),
    ('about-uk/why-choose-uk', 'about-uk', 'why-choose-the-uk'),
    ('about-uk/some-other-page', 'about-uk', ''),
    ('industries', 'about-uk', 'industries'),
    ('industries/energy', 'about-uk', 'industries'),
    ('how-to-setup-in-the-uk', 'expand', 'how-to-expand'),
    ('how-to-setup-in-the-uk/article-name', 'expand', 'how-to-expand'),
    ('expand/contact', 'expand', 'contact-us-expand'),
    ('expand', 'expand', 'overview-expand'),
    ('expand/some-other-page', 'expand', ''),
    ('opportunities', 'invest-capital', 'investment-opportunities'),
    ('opportunities/an-opportunity', 'invest-capital', 'investment-opportunities'),
    ('capital-invest/contact', 'invest-capital', 'contact-us-invest-capital'),
    ('capital-invest/contact/success', 'invest-capital', 'contact-us-invest-capital'),
    ('capital-invest', 'invest-capital', 'overview-invest-capital'),
    ('capital-invest/some-other-page', 'invest-capital', ''),
    ('trade', 'trade', 'find-a-supplier'),
    ('trade/search', 'trade', 'find-a-supplier'),
    ('trade/contact', 'trade', 'contact-us-trade'),
    ('about-us', 'about-us', 'overview-about-dit'),
    ('about-us/some-other-page', 'about-us', ''),
    ('about-us/contact', 'about-us', 'contact-us-about-dit'),
])
def test_get_header_config(path, expected_section_name, expected_sub_section_name):
    header_config = get_header_config(path)

    section = header_config.section.name if header_config.section else ''
    sub_section = header_config.sub_section.name if header_config.sub_section else ''

    assert section == expected_section_name
    assert sub_section == expected_sub_section_name
