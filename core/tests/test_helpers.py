import pytest

from django.urls import reverse

from core import helpers
from core.helpers import SortFilter, sort_opportunities, ScaleFilter, \
    filter_opportunities, RegionFilter, SectorFilter


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
    filters = {'page': 2}

    assert helpers.get_paginator_url(filters, 'opportunities') == (
        reverse('opportunities') + '?'
    )


def test_get_paginator_url_with_filters():
    filters = {'page': 2, 'sector': ['Energy', 'Aerospace']}

    assert helpers.get_paginator_url(filters, 'opportunities') == (
        reverse('opportunities') + '?sector=Energy&sector=Aerospace'
    )


def test_get_paginator_url_with_spaces_filters():
    filters = {'page': 2, 'sector': 'A value with spaces '}

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

    sorting_chosen = SortFilter('Scale: High to Low')

    sorted_opps = sort_opportunities(opportunities, sorting_chosen)

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

    sorting_chosen = SortFilter('Project name: A to Z')

    sorted_opps = sort_opportunities(opportunities, sorting_chosen)

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

    filter_chosen = ScaleFilter('< £100m')

    filtered_opps = filter_opportunities(opportunities, filter_chosen)
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
            'scale_value': 0
        },
        {
            'scale_value': 3000
        }
    ]

    filter_chosen = ScaleFilter('Value unknown')

    filtered_opps = filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 1


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

    filter_chosen = ScaleFilter('> £1bn')

    filtered_opps = filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 1


def test_filter_opportunities_region():
    opportunities = [
        {'related_region': {'title': 'Midlands'}},
        {'related_region': {'title': 'South of England'}},
        {'related_region': {'title': 'Midlands'}},
        {'related_region': {'title': ''}},
    ]

    filter_chosen = RegionFilter('Midlands')

    filtered_opps = filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 2


def test_filter_opportunities_sector():
    opportunities = [
        {
            'related_sectors': [
                {'related_sector': {'title': 'Aston Green'}},
                {'related_sector': {'title': 'Birmingham Curzon'}},
            ],
        },
        {
            'related_sectors': [
                {'related_sector': {'title': 'Aston Green'}},
            ],
        },
    ]

    filter_chosen = SectorFilter('Birmingham Curzon')

    filtered_opps = filter_opportunities(opportunities, filter_chosen)
    assert len(filtered_opps) == 1


def test_filter_opportunities_multiple_filters():
    opportunities = [
        {
            'title': 'this one',
            'related_sectors': [
                {'related_sector': {'title': ''}},
                {'related_sector': {'title': 'Birmingham Curzon'}},
            ],
            'scale_value': 0,
            'related_region': {'title': 'Midlands'},

        },
        {
            'title': 'not this one',
            'related_sectors': [
                {'related_sector': {'title': 'Aston Green'}},
            ],
            'scale_value': 3000,
            'related_region': {'title': ''},
        },
    ]

    filtered_opps = filter_opportunities(opportunities, SectorFilter(
        'Birmingham Curzon'
    ))
    filtered_opps = filter_opportunities(filtered_opps, RegionFilter(
        'Midlands'
    ))
    filtered_opps = filter_opportunities(filtered_opps, ScaleFilter(
        'Value unknown'
    ))
    assert len(filtered_opps) == 1
    assert filtered_opps[0]['title'] == 'this one'
