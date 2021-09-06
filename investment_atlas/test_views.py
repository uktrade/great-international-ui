from unittest.mock import patch

from core.tests.helpers import create_response

from investment_atlas.views import InvestmentOpportunitySearchView


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_region_sector_scale_filter_for_opportunity_search(
    mock_cms_response,
    rf,
):
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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 2',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 3',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '0.00',
                'related_regions': [
                    {
                        'title': 'South of Engalnd'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/investment/opportunities/?sector=Aerospace&scale=Value+unknown&region=Midlands'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/?sector=Aerospace&scale=Value+unknown&region=Midlands'
    )

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_num_of_opportunities_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'South of England'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 2',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/investment/opportunities/?sector=Aerospace')
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request, path='/international/investment/opportunities?sector=Aerospace')

    assert response.context_data['num_of_opportunities'] == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_filters_chosen_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'South of England'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/investment/opportunities/?scale=<+£100m')
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request, path='/international/investment/opportunities/?scale=<+£100m')

    assert len(response.context_data['filters']) == 1
    assert '< £100m' in response.context_data['filters']


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_sorting_filters_chosen_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'South of England'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/investment/opportunities/?sort_by=Scale%3A+Low+to+High&region=Midlands'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/?sort_by=Scale%3A+Low+to+High&regionMidlands'
    )

    assert response.context_data['sorting_chosen'] == 'Scale: Low to High'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_sub_sector_filters_chosen_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'South of England'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/investment/opportunities/?sub_sector=housing')
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/?sub_sector=housing'
    )

    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'
    assert len(response.context_data['pagination'].object_list) == 1


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_goes_to_page_one_if_page_num_too_big_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'related_regions': [
                    {
                        'title': 'South of England'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/investment/opportunities/?page=10'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/'
             '?page=10'
    )

    assert response.url == '/international/investment/opportunities/?&page=1'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_goes_to_page_one_if_page_num_not_a_num_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'related_regions': [
                    {
                        'title': 'South of England'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/investment/opportunities/?page=qq'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/?page=qq'
    )

    assert response.url == '/international/investment/opportunities/?&page=1'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_sub_sectors_being_shown_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
        'sector_with_sub_sectors': {
            'Aerospace': ['Commercial'],
            'Automotive': [],
            'Real Estate': ['Housing', 'Commercial', 'Mixed use']
        },
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['Commercial', 'Housing'],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'South of England'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': [],
                'scale_value': '1000.00',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['Housing', 'Commercial', 'Mixed use'],
                'scale_value': '1000.00',
                'related_regions':
                [
                    {
                        'title': 'Midlands'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Real Estate'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request_no_sector_chosen = rf.get(
        '/international/investment/opportunities/?'
    )
    request_no_sector_chosen.LANGUAGE_CODE = 'en-gb'
    response_no_sector_chosen = InvestmentOpportunitySearchView.as_view()(
        request_no_sector_chosen,
        path='/international/investment/opportunities/?'
    )

    assert len(response_no_sector_chosen.context_data['sub_sectors']) == 3

    request_one_sector_chosen = rf.get('/international/investment/opportunities/?sector=Aerospace')
    request_one_sector_chosen.LANGUAGE_CODE = 'en-gb'
    response_one_sector_chosen = InvestmentOpportunitySearchView.as_view()(
        request_one_sector_chosen,
        path='/international/investment/opportunities/?sector=Aerospace'
    )

    assert len(response_one_sector_chosen.context_data['sub_sectors']) == 1
    for sub_sector in response_one_sector_chosen.context_data['sub_sectors']:
        assert 'Commercial' in sub_sector

    request_two_sectors_chosen = rf.get(
        '/international/investment/opportunities/?sector=Real+Estate&sector=Aerospace'
    )
    request_two_sectors_chosen.LANGUAGE_CODE = 'en-gb'
    response_two_sectors_chosen = InvestmentOpportunitySearchView.as_view()(
        request_two_sectors_chosen,
        path='/international/investment/opportunities/?sector=Real+Estate&sector=Aerospace'
    )

    assert len(response_two_sectors_chosen.context_data['sub_sectors']) == 3

    request_sectors_and_sub_sectors_chosen = rf.get(
        '/international/investment/opportunities/?sector=Aerospace&sub_sector=Housing'
    )
    request_sectors_and_sub_sectors_chosen.LANGUAGE_CODE = 'en-gb'
    response_sectors_and_sub_sectors_chosen = InvestmentOpportunitySearchView.as_view()(
        request_sectors_and_sub_sectors_chosen,
        path='/international/investment/opportunities/?sector=Aerospace&sub_sector=Housing'
    )

    assert len(response_sectors_and_sub_sectors_chosen.context_data['sub_sectors']) == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_when_no_opportunity_list_in_page_for_opportunity_search(
    mock_cms_response,
    rf,
):

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
        'page_type': 'InvestmentOpportunityListingPage',
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get('/international/investment/opportunities/')
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request, path='/international/investment/opportunities/')

    assert response.context_data['num_of_opportunities'] == 0


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_investment_type_filter_for_opportunity_search(
    mock_cms_response,
    rf,
):
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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'investment_type': 'Investment Type One',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 2',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'investment_type': 'Investment Type Two',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 3',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '0.00',
                'investment_type': 'Investment Type One',
                'related_regions': [
                    {
                        'title': 'South of Engalnd'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/investment/opportunities/?investment_type=Investment+Type+One'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/?investment_type=Investment+Type+One'
    )

    assert len(response.context_data['pagination'].object_list) == 2
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'
    assert response.context_data['pagination'].object_list[1]['title'] == 'Some Opp 3'

    # Extra test coverage of all_investment_types
    view = InvestmentOpportunitySearchView()
    view.page = page
    assert view.all_investment_types() == [
        ('Investment Type One', 'Investment Type One'),
        ('Investment Type Two', 'Investment Type Two'),
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_planning_status_filter_for_opportunity_search(
    mock_cms_response,
    rf,
):
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
        'page_type': 'InvestmentOpportunityListingPage',
        'opportunity_list': [
            {
                'id': 6,
                'title': 'Some Opp 1',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '',
                'investment_type': 'Investment Type One',
                'planning_status': 'Planning Status Two',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Aerospace'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 2',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '1000.00',
                'investment_type': 'Investment Type Two',
                'planning_status': 'Planning Status Five',
                'related_regions': [
                    {
                        'title': 'Midlands'
                    }
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
            {
                'id': 4,
                'title': 'Some Opp 3',
                'sub_sectors': ['energy', 'housing-led'],
                'scale_value': '0.00',
                'investment_type': 'Investment Type One',
                'planning_status': 'Planning Status Five',
                'related_regions': [
                    {
                        'title': 'South of Engalnd'
                    },
                ],
                'related_sectors': [
                    {
                        'related_sector': {
                            'heading': 'Automotive'
                        }
                    },
                ],
            },
        ]
    }

    mock_cms_response.return_value = create_response(page)

    request = rf.get(
        '/international/investment/opportunities/?planning_status=Planning+Status+Five'
    )
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(
        request,
        path='/international/investment/opportunities/?planning_status=Planning+Status+Five'
    )

    assert len(response.context_data['pagination'].object_list) == 2
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 2'
    assert response.context_data['pagination'].object_list[1]['title'] == 'Some Opp 3'

    # Extra test coverage of all_planning_statuses
    view = InvestmentOpportunitySearchView()
    view.page = page
    assert view.all_planning_statuses() == [
        ('Planning Status Five', 'Planning Status Five'),
        ('Planning Status Two', 'Planning Status Two'),
    ]
