import pytest
from unittest.mock import call, patch
from importlib import import_module
from requests.exceptions import HTTPError
from django.urls import reverse
from django.test import RequestFactory

from directory_constants import choices

from core.tests.helpers import create_response
from investment_atlas import views
from investment_atlas.forms import HOW_CAN_WE_HELP_CHOICES, HOW_DID_YOU_HEAR_CHOICES
from investment_atlas.views import InvestmentOpportunitySearchView


def create_opportunities_page():
    mock_page = {
        'title': 'Investment opportunities',
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
                'id': 1,
                'title': 'Some Opp 1',
                'sub_sectors': ['Energy', 'Housing'],
                'scale_value': '',
                'investment_type': 'Foreign direct investment',
                'planning_status': 'Planning Status Two',
                'related_regions': [{'title': 'Midlands'}],
                'related_sectors': [{'related_sector': {'heading': 'Aerospace'}}, ],
            },
            {
                'id': 2,
                'title': 'Some Opp 2',
                'sub_sectors': ['Energy', 'Building'],
                'scale_value': '1000.00',
                'investment_type': 'Foreign direct investment',
                'planning_status': 'Planning Status Five',
                'related_regions': [{'title': 'Scotland'}],
                'related_sectors': [{'related_sector': {'heading': 'Automotive'}}, ],
            },
            {
                'id': 3,
                'title': 'Some Opp 3',
                'sub_sectors': ['Energy'],
                'scale_value': '0.00',
                'investment_type': 'Capital investment - energy and infrastructure',
                'planning_status': 'Planning Status Five',
                'related_regions': [{'title': 'South of England'}, ],
                'related_sectors': [{'related_sector': {'heading': 'Aerospace'}}, ],
            },
            {
                'id': 4,
                'title': 'Some Opp 4',
                'sub_sectors': ['Energy'],
                'scale_value': '0.00',
                'investment_type': 'Capital investment - energy and infrastructure',
                'planning_status': 'Planning Status Two',
                'related_regions': [{'title': 'South of England'}, ],
                'related_sectors': [{'related_sector': {'heading': 'Aerospace'}}, ],
            },
            {
                'id': 5,
                'title': 'Some Opp 5',
                'sub_sectors': ['Energy'],
                'scale_value': '0.00',
                'investment_type': 'Capital investment - real estate',
                'planning_status': 'Planning Status Two',
                'related_regions': [{'title': 'Northern Ireland'}, ],
                'related_sectors': [{'related_sector': {'heading': 'Aerospace'}}, ],
            },
        ]
    }

    # Add further non-related opportunities
    for index in range(6, 16):
        mock_page['opportunity_list'].append({
            'id': index,
            'title': 'Some Opp {}'.format(index),
            'sub_sectors': ['Chemicals', 'Nuclear'],
            'scale_value': '0.00',
            'investment_type': 'Capital investment - real estate',
            'planning_status': 'Planning Status Two',
            'related_regions': [{'title': 'Wales'}, ],
            'related_sectors': [{'related_sector': {'heading': 'Agriculture'}}, ],
        })

    return mock_page


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def create_opportunities_response(page, path, mock_cms_response):
    mock_cms_response.return_value = create_response(page)

    rf = RequestFactory()
    request = rf.get(path)
    request.LANGUAGE_CODE = 'en-gb'
    response = InvestmentOpportunitySearchView.as_view()(request, path=path)

    return response


def test_atlas_opportunities_num_of_results():
    page = create_opportunities_page()

    response = create_opportunities_response(page, '/international/investment/opportunities/')

    assert len(response.context_data['pagination'].object_list) == 10
    assert response.context_data['num_of_opportunities'] == 15

    # Collapse consecutive whitespace
    rendered = ' '.join(response.rendered_content.split())
    assert '15 opportunities found' in rendered


def test_atlas_opportunities_num_of_results_singular():
    page = create_opportunities_page()

    # Truncate opportunity list to one result
    page['opportunity_list'] = [page['opportunity_list'][0]]

    response = create_opportunities_response(page, '/international/investment/opportunities/')

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['num_of_opportunities'] == 1

    # Collapse consecutive whitespace
    rendered = ' '.join(response.rendered_content.split())
    assert '1 opportunity found' in rendered


def test_atlas_opportunities_num_of_results_includes_investment_type_selected():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/?investment_type=Foreign+direct+investment'
    )

    assert response.context_data['num_of_opportunities'] == 2
    # Collapse consecutive whitespace
    rendered = ' '.join(response.rendered_content.split())
    assert 'aria-label="Change investment type"' in rendered
    assert 'foreign direct investment' in rendered
    assert ' opportunities found' in rendered


def test_get_sorting_filters_chosen_for_opportunity_search():
    page = create_opportunities_page()

    response = create_opportunities_response(page,
                                             '/international/investment/opportunities/?sort_by=Scale%3A+Low+to+High')

    assert response.context_data['sorting_chosen'] == 'Scale: Low to High'


def test_goes_to_page_one_if_page_num_too_big_for_opportunity_search():
    page = create_opportunities_page()

    response = create_opportunities_response(page, '/international/investment/opportunities/?page=10')

    assert response.url == '/international/investment/opportunities/?&page=1'


def test_goes_to_page_one_if_page_num_not_a_num_for_opportunity_search():
    page = create_opportunities_page()

    response = create_opportunities_response(page, '/international/investment/opportunities/?page=qq')

    assert response.url == '/international/investment/opportunities/?&page=1'


def test_when_no_opportunity_list_in_page_for_opportunity_search():
    page = create_opportunities_page()
    page.pop('opportunity_list', None)

    response = create_opportunities_response(page, '/international/investment/opportunities/')

    assert response.context_data['num_of_opportunities'] == 0


def test_atlas_opportunities_shows_only_investment_type_selector():
    page = create_opportunities_page()

    response = create_opportunities_response(page, '/international/investment/opportunities/')

    assert response.context_data['selected_investment_type'] is None
    assert 'Choose investment type' in response.rendered_content
    assert 'Foreign direct investment' in response.rendered_content
    assert 'Capital investment - energy and infrastructure' in response.rendered_content
    assert 'Asset class' not in response.rendered_content
    assert 'UK nation or region' not in response.rendered_content
    assert 'Clear all filters' not in response.rendered_content
    assert 'Update results' not in response.rendered_content


def test_investment_type_filter_for_opportunity_search():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/?investment_type=Foreign+direct+investment'
    )

    assert len(response.context_data['pagination'].object_list) == 2
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'
    assert response.context_data['pagination'].object_list[1]['title'] == 'Some Opp 2'


def test_atlas_opportunities_ignores_other_filters_if_no_investment_type_selected():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/?sector=Automotive&region=South+of+England&sub_sector=Chemicals'
    )

    assert len(response.context_data['pagination'].object_list) == 10
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'
    assert response.context_data['form']['region'].initial == []
    assert response.context_data['form']['sector'].initial == []
    assert response.context_data['form']['sub_sector'].initial == []

    assert response.context_data['form'].fields['region'].choices == []
    assert response.context_data['form'].fields['sector'].choices == []
    assert response.context_data['form'].fields['sub_sector'].choices == []


def test_atlas_opportunities_shows_sector_with_count_and_region_filters_for_foreign_direct_investment_search():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/?investment_type=Foreign+direct+investment'
    )

    assert response.context_data['form'].fields['sector'].choices == [
        ('Aerospace', 'Aerospace (1)'),
        ('Automotive', 'Automotive (1)'),
    ]
    assert response.context_data['form'].fields['region'].choices == [
        ('Midlands', 'Midlands'),
        ('Scotland', 'Scotland'),
    ]
    assert response.context_data['form'].fields['sub_sector'].choices == []


def test_atlas_opportunities_shows_sub_sector_with_count_and_regions_filters_for_not_foreign_direct_investment_type():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/?investment_type=Capital+investment+-+real+estate'
    )

    assert response.context_data['selected_investment_type'] == 'Capital investment - real estate'

    assert response.context_data['form'].fields['sub_sector'].choices == [
        ('Chemicals', 'Chemicals (10)'),
        ('Energy', 'Energy (1)'),
        ('Nuclear', 'Nuclear (10)'),
    ]
    assert response.context_data['form'].fields['region'].choices == [
        ('Northern Ireland', 'Northern Ireland'),
        ('Wales', 'Wales'),
    ]
    assert response.context_data['form'].fields['sector'].choices == []


@pytest.mark.skip(
    "The planning status and scales filters are currently disabled."
)
def test_planning_status_filter_for_opportunity_search():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/' +
        '?investment_type=Foreign+direct+investment&planning_status=Planning+Status+Five'
    )

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 2'

    # Extra test coverage of all_planning_statuses
    view = InvestmentOpportunitySearchView()
    view.page = page
    assert view.all_planning_statuses() == [
        ('Planning Status Five', 'Planning Status Five'),
        ('Planning Status Two', 'Planning Status Two'),
    ]


def test_atlas_opportunities_shows_selected_filters():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/' +
        '?investment_type=Foreign+direct+investment&sector=Automotive&sector=Aerospace&region=Midlands'
    )

    assert 'Automotive' in response.context_data['filters_chosen']
    assert 'Aerospace' in response.context_data['filters_chosen']
    assert 'Midlands' in response.context_data['regions_chosen']


def test_atlas_opportunities_applies_region_filter():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/' +
        '?investment_type=Foreign+direct+investment&region=Midlands'
    )

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 1'


def test_atlas_opportunities_applies_sector_filter():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/' +
        '?investment_type=Foreign+direct+investment&sector=Automotive'
    )

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 2'


def test_atlas_opportunities_applies_sub_sector_filter():
    page = create_opportunities_page()

    response = create_opportunities_response(
        page,
        '/international/investment/opportunities/' +
        '?investment_type=Capital+investment+-+real+estate&sub_sector=Energy'
    )

    assert len(response.context_data['pagination'].object_list) == 1
    assert response.context_data['pagination'].object_list[0]['title'] == 'Some Opp 5'


def test_atlas_opportunities_defaults_to_list_with_feature_off(settings):
    settings.FEATURE_FLAGS['ATLAS_OPPORTUNITIES_MAP_ON'] = False

    page = create_opportunities_page()

    response = create_opportunities_response(page, '/international/investment/opportunities/?view=map')

    assert response.context_data['form']['view'].value() == 'list'
    assert 'id="atlas-opportunities-map"' not in response.rendered_content
    assert 'atlas-search--as-map' not in response.rendered_content
    assert 'id="id_view"' not in response.rendered_content


def test_atlas_opportunities_map_view_shows_all_results(settings):
    settings.FEATURE_FLAGS['ATLAS_OPPORTUNITIES_MAP_ON'] = True
    settings.ATLAS_OPPORTUNITIES_MAP_POOL_ID = 'FOO-BAR-POOL-ID'

    page = create_opportunities_page()

    response = create_opportunities_response(page, '/international/investment/opportunities/?view=map')

    assert response.context_data['aws_cognito_pool_id'] == 'FOO-BAR-POOL-ID'
    assert 'id="id_view"' in response.rendered_content
    assert 'id="atlas-opportunities-map"' in response.rendered_content
    assert 'atlas-search--as-map' in response.rendered_content
    assert len(response.context_data['pagination'].object_list) == 15


def test_atlas_opportunities_map_view_shows_no_results_as_list(settings):
    settings.FEATURE_FLAGS['ATLAS_OPPORTUNITIES_MAP_ON'] = True

    page = create_opportunities_page()
    page.pop('opportunity_list', None)

    response = create_opportunities_response(page, '/international/investment/opportunities/?view=map')

    assert 'No results' in response.rendered_content
    assert 'atlas-search--as-map' not in response.rendered_content


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_opportunity_detail(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'meta': {'languages': [['en-gb', 'English']]},
            'page_type': 'InvestmentOpportunityPage',
        }
    )

    url = '/international/content/investment/opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'investment_atlas/opportunity.html'
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_opportunity_detail_not_found(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(status_code=404)

    url = '/international/content/investment/opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_opportunity_detail_cms_retrieval_ok(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'title': '1234',
            'meta': {'languages': [['en-gb', 'English']]},
            'page_type': 'InvestmentOpportunityPage',
        }
    )

    url = '/international/content/investment/opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page'] == {
        'title': '1234', 'meta': {'languages': [['en-gb', 'English']]},
        'page_type': 'InvestmentOpportunityPage',
    }


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_opportunity_detail_cms_retrieval_not_ok(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(status_code=400)

    url = '/international/content/investment/opportunities/rail/'

    with pytest.raises(HTTPError):
        client.get(url)


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_foreign_direct_investment_form(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(
        json_payload={
            'opportunity_list': [],
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'ForeignDirectInvestmentFormPage',
        }
    )

    url = reverse('fdi-opportunity-request-form')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.ForeignDirectInvestmentOpportunityFormView.template_name
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_foreign_direct_investment_form_not_found(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(status_code=404)

    url = reverse('fdi-opportunity-request-form')
    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_foreign_direct_investment_form_cms_retrieval_ok(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'opportunity_list': [
                {
                    # 'pdf_document': 'http://www.example.com/a',  # Disabled for now
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail', 'url': 'http://www.example.com/test/opp/'}
                }
            ],
            'page_type': 'ForeignDirectInvestmentFormPage',
        }
    )

    url = reverse('fdi-opportunity-request-form')

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['opportunities'].choices == [
        ('http://www.example.com/test/opp/', 'some great opportunity'),
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_foreign_direct_investment_form_cms_retrieval_not_ok(mock_lookup_by_path, client):
    mock_lookup_by_path.return_value = create_response(status_code=400)

    url = reverse('fdi-opportunity-request-form')

    with pytest.raises(HTTPError):
        client.get(url)


@patch('investment_atlas.forms.ForeignDirectInvestmentOpportunityForm.action_class')
@patch('investment_atlas.forms.ForeignDirectInvestmentOpportunityForm.action_class.save')
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_foreign_direct_investment_form_submmit_cms_retrieval_ok(mock_lookup_by_path, mock_save, mock_action_class,
                                                                 settings, rf, captcha_stub):
    mock_lookup_by_path.return_value = create_response(
        json_payload={
            'opportunity_list': [
                {
                    # 'pdf_document': 'http://www.example.com/a',  # Disabled for now
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail', 'url': 'http://www.example.com/test/opp/'}
                }
            ],
            'page_type': 'ForeignDirectInvestmentFormPage',
        }
    )
    mock_save.return_value = create_response(status_code=200)
    settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS = 'invest@example.com'

    url = reverse('fdi-opportunity-request-form')

    request = rf.post(url, data={
        'given_name': 'Jim',
        'family_name': 'Example',
        'job_title': 'Chief chief',
        'email_address': 'test@example.com',
        'phone_number': '555',
        'company_name': 'Example corp',
        'website_url': 'example.com',
        'company_address': '123 Some Street, \nSome town, \nSomewhere, \nNarnia',
        'country': choices.COUNTRY_CHOICES[1][0],
        'industry': [choices.INDUSTRIES[0][0]],
        'opportunities': [
            'http://www.example.com/test/opp/',
        ],
        'how_can_we_help': HOW_CAN_WE_HELP_CHOICES[0][0],
        'your_plans': 'Lorem ipsum dolor sit amet',
        'how_did_you_hear': HOW_DID_YOU_HEAR_CHOICES[0][0],
        'email_contact_consent': True,
        'telephone_contact_consent': True,
        'g-recaptcha-response': captcha_stub,
    })

    utm_data = {
        'campaign_source': 'test_source',
        'campaign_medium': 'test_medium',
        'campaign_name': 'test_campaign',
        'campaign_term': 'test_term',
        'campaign_content': 'test_content'
    }
    request.utm = utm_data
    request.session = {}
    response = views.ForeignDirectInvestmentOpportunityFormView.as_view()(
        request,
        path='/invest/high-potential-opportunities/contact/success/',
    )

    assert response.status_code == 302
    assert response.url == reverse('fdi-opportunity-request-form-success')

    assert mock_action_class.call_args_list[0] == call(
        email_address=settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS,
        template_id=settings.HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID,
        form_url=url,
        sender={'email_address': 'test@example.com', 'country_code': 'AL', 'ip_address': '127.0.0.1'}
    )
    assert mock_action_class.call_args_list[1] == call(
        email_address='test@example.com',
        template_id=settings.HPO_GOV_NOTIFY_USER_TEMPLATE_ID,
        form_url=url,
        email_reply_to_id=settings.HPO_GOV_NOTIFY_USER_REPLY_TO_ID,
    )


@pytest.mark.skip(
    "Skipped because we're currently not redirecting if there is no session data, "
    "because we don't need that data until we start passing around PDF download URLs again"
)
def test_foreign_direct_investment_form_get_success_page_no_session(client):
    url = reverse('fdi-opportunity-request-form-success')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('fdi-opportunity-request-form')


@pytest.mark.skip(
    "Skipped because we're currently not parking selected opps in session data, "
    "because we don't need that data until we start passing around PDF download URLs again"
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_foreign_direct_investment_form_get_success_page_with_session(mock_lookup_by_path, settings, client):
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    session = store
    client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    session[views.SESSION_KEY_SELECTED_OPPORTUNITIES] = (
        'http://www.example.com/a'
    )
    session.save()

    mock_lookup_by_path.return_value = create_response(
        json_payload={
            'opportunity_list': [
                {
                    # 'pdf_document': 'http://www.example.com/a',  # Disabled for now
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail', 'url': 'http://www.example.com/test/opp/'}
                },
                {
                    # 'pdf_document': 'http://www.example.com/b',  # Disabled for now
                    'heading': 'some other opportunity',
                    'meta': {'slug': 'other', 'url': 'http://www.example.com/test/other-opp/'}
                }
            ],
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'ForeignDirectInvestmentFormSuccessPage',
        }
    )

    url = reverse('fdi-opportunity-request-form-success')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page']

    assert response.context_data['opportunities'] == [
        {
            'pdf_document': 'http://www.example.com/a',
            'heading': 'some great opportunity',
            'meta': {'slug': 'rail', 'url': 'http://www.example.com/test/opp/'}
        }
    ]
