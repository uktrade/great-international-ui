from unittest import mock

from directory_api_client.client import api_client
from directory_constants import expertise
import pytest
import requests

from django.urls import reverse

from core.helpers import CompanyParser, get_case_study_details_from_response
from core.tests.helpers import create_response
from investment_support_directory import forms, views


@pytest.fixture(autouse=True)
def mock_retrieve_company(retrieve_profile_data):
    patch = mock.patch.object(
        api_client.company, 'published_profile_retrieve',
        return_value=create_response(retrieve_profile_data)
    )
    yield patch.start()
    patch.stop()


@pytest.fixture()
def mock_retrieve_company_non_isd(retrieve_profile_data):
    retrieve_profile_data['is_published_investment_support_directory'] = False
    patch = mock.patch.object(
        api_client.company, 'published_profile_retrieve',
        return_value=create_response(retrieve_profile_data)
    )
    yield patch.start()
    patch.stop()


def test_profile(client, retrieve_profile_data):
    company = CompanyParser(retrieve_profile_data)

    url = reverse(
        'investment-support-directory:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['company'] == company.serialize_for_template()


def test_profile_querystring(client, retrieve_profile_data):
    company = CompanyParser(retrieve_profile_data)

    url = reverse(
        'investment-support-directory:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url, {'q': '123'})

    assert response.status_code == 200
    assert response.context_data['company'] == company.serialize_for_template()
    assert response.context_data['search_querystring'] == 'q=123'


def test_profile_slug_redirect(client, retrieve_profile_data):
    url = reverse(
        'investment-support-directory:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': 'something',
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse(
        'investment-support-directory:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )


def test_trade_redirect(client):

    url = '/international/trade/investment-support-directory/search/'
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == '/international/investment-support-directory/'


def test_profile_calls_api(
    mock_retrieve_company, client, retrieve_profile_data
):
    url = reverse(
        'investment-support-directory:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == 200
    assert mock_retrieve_company.call_count == 1
    assert mock_retrieve_company.call_args == mock.call(
        number=retrieve_profile_data['number']
    )


def test_get_profile_404_non_investment_support_directory(
    mock_retrieve_company_non_isd, client, retrieve_profile_data
):
    url = reverse(
        'investment-support-directory:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == 404


def test_home_page_context_data(client):
    url = reverse('investment-support-directory:home')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['CHOICES_FINANCIAL'] == expertise.FINANCIAL
    assert response.context_data['CHOICES_HUMAN_RESOURCES'] == (
        expertise.HUMAN_RESOURCES
    )
    assert response.context_data['CHOICES_LEGAL'] == expertise.LEGAL
    assert response.context_data['CHOICES_PUBLICITY'] == expertise.PUBLICITY
    assert response.context_data['CHOICES_BUSINESS_SUPPORT'] == (
        expertise.BUSINESS_SUPPORT
    )
    assert response.context_data['CHOICES_MANAGEMENT_CONSULTING'] == (
        expertise.MANAGEMENT_CONSULTING
    )


def test_home_page_redirect(client):
    url = reverse('investment-support-directory:home')
    expected_url = reverse('investment-support-directory:search')

    response = client.post(url, {'q': 'foo'})

    assert response.status_code == 302
    assert response.url == f'{expected_url}?q=foo'


def test_home_page_show_guide(client):
    url = reverse('investment-support-directory:search')

    response = client.get(url, {'show-guide': True})

    assert response.status_code == 200
    assert response.context_data['show_search_guide'] is True


@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_home_page_hide_guide(mock_get_results_and_count, client):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    url = reverse('investment-support-directory:search')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['show_search_guide'] is False


@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_search_submit_form_on_get(mock_get_results_and_count, client, search_results):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(
        reverse('investment-support-directory:search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert response.context_data['results'] == results


@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_company_search_pagination_count(mock_get_results_and_count, client, search_results):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(
        reverse('investment-support-directory:search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert response.context_data['pagination'].paginator.count == 20


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_pagination_param(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    url = reverse('investment-support-directory:search')
    response = client.get(
        url, {'q': '123', 'page': 1, 'expertise_industries': ['AEROSPACE']}
    )

    assert response.status_code == 200
    assert mock_search.call_count == 1
    assert mock_search.call_args == mock.call(
        expertise_countries=[],
        expertise_financial=None,
        expertise_industries=['AEROSPACE'],
        expertise_languages=[],
        expertise_products_services_labels=[],
        expertise_regions=[],
        page=1,
        size=10,
        term='123'
    )


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_pagination_empty_page(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    url = reverse('investment-support-directory:search')
    response = client.get(url, {'q': '123', 'page': 100})

    assert response.status_code == 302
    assert response.get('Location') == (
        reverse('investment-support-directory:search') + '?q=123'
    )


@mock.patch.object(api_client.company, 'search_investment_search_directory')
@mock.patch.object(views, 'get_results_from_search_response')
def test_company_search_not_submit_without_params(
    mock_get_results_from_search_response, mock_search, client, search_results
):
    mock_search.return_value = api_response = create_response(search_results)
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(reverse('investment-support-directory:search'))

    assert response.status_code == 200
    assert mock_get_results_from_search_response.call_count == 1
    assert mock_get_results_from_search_response.call_args == mock.call(api_response)


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_api_call_error(mock_search, client):
    mock_search.return_value = create_response(status_code=400)

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(
            reverse('investment-support-directory:search'), {'q': '123'}
        )


@mock.patch.object(api_client.company, 'search_investment_search_directory')
@mock.patch.object(views, 'get_results_from_search_response')
def test_company_search_api_success(
    mock_get_results_from_search_response, mock_search, client, search_results
):
    mock_search.return_value = api_response = create_response(search_results)
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(
        reverse('investment-support-directory:search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert mock_get_results_from_search_response.call_count == 1
    assert mock_get_results_from_search_response.call_args == mock.call(api_response)


@mock.patch.object(api_client.company, 'search_investment_search_directory')
@mock.patch('core.helpers.get_results_from_search_response')
def test_company_search_querystring(
    mock_get_results_from_search_response, mock_search, client, search_results
):
    mock_search.return_value = create_response(search_results)
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(
        reverse('investment-support-directory:search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert response.context_data['search_querystring'] == 'q=123'


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_response_no_highlight(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    response = client.get(
        reverse('investment-support-directory:search'), {'q': 'wolf'}
    )

    assert b'this is a short summary' in response.content


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_highlight_description(
    mock_search, search_results_description_highlight, client,
):
    mock_search.return_value = create_response(search_results_description_highlight)

    response = client.get(
        reverse('investment-support-directory:search'), {'q': 'wolf'}
    )
    expected = (
        b'<em>wolf</em> in sheep clothing description...'
        b'to the max <em>wolf</em>.'
    )

    assert expected in response.content


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_highlight_summary(
    mock_search, search_results_summary_highlight, client
):
    mock_search.return_value = create_response(search_results_summary_highlight)

    response = client.get(
        reverse('investment-support-directory:search'), {'q': 'wolf'}
    )

    assert b'<em>wolf</em> in sheep clothing summary.' in response.content


@mock.patch.object(forms.ContactCompanyForm, 'save')
def test_contact_company(mock_save, client, settings, captcha_stub, retrieve_profile_data):
    url = reverse(
        'investment-support-directory:company-contact',
        kwargs={'company_number': 'ST121'}
    )
    success_url = reverse(
        'investment-support-directory:company-contact-sent',
        kwargs={'company_number': 'ST121'}
    )
    data = {
        'given_name': 'Jim',
        'family_name': 'Example',
        'company_name': 'Example corp',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'subject': 'Hello',
        'body': 'foo bar bax',
        'has_contact': True,
        'terms': True,
        'g-recaptcha-response': captcha_stub,
    }
    response = client.post(f'{url}?q=123', data)

    assert response.status_code == 302
    assert response.url == f'{success_url}?q=123'

    assert mock_save.call_count == 3
    assert mock_save.call_args_list[0] == mock.call(
        email_address=retrieve_profile_data['email_address'],
        form_url=url,
        sender={'email_address': 'jim@example.com', 'country_code': None, 'ip_address': '127.0.0.1'},
        spam_control={'contents': ['Hello', 'foo bar bax']},
        template_id=settings.CONTACT_ISD_COMPANY_NOTIFY_TEMPLATE_ID,
    )
    assert mock_save.call_args_list[1] == mock.call(
        form_url=f'{url}?q=123',
        email_address=settings.CONTACT_ISD_SUPPORT_EMAIL_ADDRESS,
        template_id=settings.CONTACT_ISD_SUPPORT_NOTIFY_TEMPLATE_ID,
    )
    assert mock_save.call_args_list[2] == mock.call(
        email_address=data['email_address'],
        form_url=f'{url}?q=123',
        spam_control={'contents': ['Hello', 'foo bar bax']},
        template_id=settings.CONTACT_ISD_INVESTOR_NOTIFY_TEMPLATE_ID,
    )


def test_contact_company_success(client):
    url = reverse(
        'investment-support-directory:company-contact-sent',
        kwargs={'company_number': '01111111'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.ContactSuccessView.template_name]


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_case_study_exposes_context(
    mock_published_case_study_retrieve, client, supplier_case_study_data,
):
    mock_published_case_study_retrieve.return_value = create_response(json_payload=supplier_case_study_data)
    expected_case_study = get_case_study_details_from_response(
        create_response(json_payload=supplier_case_study_data)
    )

    url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.CaseStudyDetailView.template_name]
    assert response.context_data['case_study'] == expected_case_study
    assert response.context_data['social'] == {
        'description': expected_case_study['description'],
        'image': expected_case_study['image_one'],
        'title': 'Project: {}'.format(expected_case_study['title']),
    }


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_case_study_calls_api(
    mock_published_case_study_retrieve, client, supplier_case_study_data,
):
    mock_published_case_study_retrieve.return_value = create_response(json_payload=supplier_case_study_data)
    url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    client.get(url)

    assert mock_published_case_study_retrieve.call_count == 1
    assert mock_published_case_study_retrieve.call_args == mock.call('2')


def test_case_study_different_slug_redirected(
    supplier_case_study_data, client
):
    url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'] + 'thing',
        }
    )
    expected_redirect_url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_case_study_missing_slug_redirected(supplier_case_study_data, client):
    url = reverse(
        'investment-support-directory:case-study-details-slugless',
        kwargs={
            'id': supplier_case_study_data['pk'],
        }
    )
    expected_redirect_url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_case_study_same_slug_not_redirected(supplier_case_study_data, client):
    url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)
    assert response.status_code == 200


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_case_study_handles_bad_status(
    mock_published_case_study_retrieve, client, supplier_case_study_data
):
    mock_published_case_study_retrieve.return_value = create_response(status_code=400)
    url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_case_study_handles_404(mock_published_case_study_retrieve, client, supplier_case_study_data):
    mock_published_case_study_retrieve.return_value = create_response(status_code=404)
    url = reverse(
        'investment-support-directory:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == 404
