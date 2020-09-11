import requests
import pytest

from unittest import mock
from unittest.mock import call, patch

from django.urls import reverse, NoReverseMatch

from directory_api_client.client import api_client
from directory_constants import sectors, choices

from core.helpers import CompanyParser, get_case_study_details_from_response
from core.tests.helpers import create_response
from find_a_supplier import forms, views, constants


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_fas_homepage_search_form(mock_cms_response, fas_home_page, client):
    mock_cms_response.return_value = create_response(
        json_payload=fas_home_page.return_value.json()
    )

    url = reverse('find-a-supplier:trade-home')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['search_form'] == forms.SearchForm


@pytest.fixture()
def mock_retrieve_company_non_find_a_supplier(retrieve_profile_data):
    retrieve_profile_data['is_published_find_a_supplier'] = False
    patch = mock.patch.object(
        api_client.company, 'published_profile_retrieve',
        return_value=create_response(retrieve_profile_data)
    )
    yield patch.start()
    patch.stop()


def test_public_profile_different_slug_redirected(
    client, retrieve_profile_data
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'] + 'thing',
        }
    )
    expected_redirect_url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_public_profile_missing_slug_redirected(client, retrieve_profile_data):
    url = reverse(
        'find-a-supplier:profile-slugless',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        }
    )
    expected_redirect_url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_public_profile_same_slug_not_redirected(
    client, retrieve_profile_data
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)
    assert response.status_code == 200


def test_public_profile_details_verbose_context(client, retrieve_profile_data):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url + '?verbose=true')
    assert response.status_code == 200
    assert response.context_data['show_description'] is True


def test_public_profile_details_non_verbose_context(
    client, retrieve_profile_data
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context_data['show_description'] is False


@mock.patch.object(views.api_client.company, 'published_profile_retrieve', mock.Mock)
@mock.patch('core.helpers.get_company_profile')
def test_public_profile_details_exposes_context(
    mock_get_company_profile, client, retrieve_profile_data
):
    mock_get_company_profile.return_value = retrieve_profile_data
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug']
        },
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name == [
        views.ProfileView.template_name
    ]
    assert response.context_data['company'] == (
        CompanyParser(retrieve_profile_data).serialize_for_template()
    )
    assert response.context_data['social'] == {
        'description': retrieve_profile_data['summary'],
        'image': retrieve_profile_data['logo'],
        'title': (
            f'International trade profile: {retrieve_profile_data["name"]}'
        )
    }


def test_company_profile_list_with_params_redirects_to_search(client):
    url = reverse('find-a-supplier:public-company-profiles-list')
    response = client.get(url, {'sectors': 'AEROSPACE'})

    assert response.status_code == 302
    assert response.get('Location') == '/international/trade/search/?industries=AEROSPACE'


def test_company_profile_list_redirects_to_search(client):
    url = reverse('find-a-supplier:public-company-profiles-list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == '/international/trade/search/'


@mock.patch('core.helpers.get_company_profile')
def test_public_profile_details_calls_api(
    mock_retrieve_profile, client, retrieve_profile_data
):
    mock_retrieve_profile.return_value = retrieve_profile_data
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    client.get(url)

    assert mock_retrieve_profile.call_count == 1
    assert mock_retrieve_profile.call_args == mock.call(
        retrieve_profile_data['number']
    )


@mock.patch.object(views.api_client.company, 'published_profile_retrieve')
def test_public_profile_details_handles_bad_status(mock_published_profile_retrieve, client):
    mock_published_profile_retrieve.return_value = create_response(status_code=400)
    url = reverse(
        'find-a-supplier:profile',
        kwargs={'company_number': '01234567', 'slug': 'thing'}
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


@mock.patch.object(views.api_client.company, 'published_profile_retrieve')
def test_public_profile_details_handles_404(mock_published_profile_retrieve, client):
    mock_published_profile_retrieve.return_value = create_response(status_code=404)
    url = reverse(
        'find-a-supplier:profile',
        kwargs={'company_number': '01234567', 'slug': 'thing'}
    )

    response = client.get(url)

    assert response.status_code == 404


def test_public_profile_details_404_non_fas(
        mock_retrieve_company_non_find_a_supplier,
        client,
        retrieve_profile_data,
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 404


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_supplier_case_study_exposes_context(
    mock_published_case_study_retrieve, client, supplier_case_study_data,
):
    response = create_response(json_payload=supplier_case_study_data)
    mock_published_case_study_retrieve.return_value = response

    expected_case_study = get_case_study_details_from_response(response)
    url = reverse(
        'find-a-supplier:case-study-details',
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
def test_supplier_case_study_calls_api(
    mock_published_case_study_retrieve, client, supplier_case_study_data
):

    mock_published_case_study_retrieve.return_value = create_response(json_payload=supplier_case_study_data)
    url = reverse(
        'find-a-supplier:case-study-details',
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
        'find-a-supplier:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'] + 'thing',
        }
    )
    expected_redirect_url = reverse(
        'find-a-supplier:case-study-details',
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
        'find-a-supplier:case-study-details-slugless',
        kwargs={
            'id': supplier_case_study_data['pk'],
        }
    )
    expected_redirect_url = reverse(
        'find-a-supplier:case-study-details',
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
        'find-a-supplier:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)
    assert response.status_code == 200


def test_trade_redirect_homepage(client):
    url = reverse('trade-incoming', kwargs={'path': ''})
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/trade/?foo=bar'


def test_invest_redirect_homepage_english(client):
    url = reverse('trade-incoming-homepage')
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/trade/?foo=bar'


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_supplier_case_study_handles_bad_status(
    mock_published_case_study_retrieve, client, supplier_case_study_data
):
    mock_published_case_study_retrieve.return_value = create_response(status_code=400)
    url = reverse(
        'find-a-supplier:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


@mock.patch.object(views.api_client.company, 'published_case_study_retrieve')
def test_supplier_case_study_handles_404(mock_published_case_study_retrieve, client, supplier_case_study_data):
    mock_published_case_study_retrieve.return_value = create_response(status_code=404)
    url = reverse(
        'find-a-supplier:case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == 404


def test_contact_company_view(client, retrieve_profile_data):
    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={'company_number': retrieve_profile_data['number']},
    )
    response = client.get(url)

    assert response.status_code == 200


@mock.patch.object(views.ContactCompanyView.form_class, 'save')
def test_contact_company_view_feature_submit_forms_api_success(
    mock_save, client, valid_contact_company_data, retrieve_profile_data,
    settings
):

    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        },
    )
    response = client.post(url, valid_contact_company_data)

    assert response.status_code == 302
    assert response.url == reverse(
        'find-a-supplier:company-contact-sent',
        kwargs={'company_number': retrieve_profile_data['number']}
    ) + '?'
    assert mock_save.call_count == 1
    assert mock_save.call_args == mock.call(
        email_address=retrieve_profile_data['email_address'],
        form_url=url,
        sender={
            'email_address': valid_contact_company_data['email_address'],
            'country_code': valid_contact_company_data['country'],
            'ip_address': '127.0.0.1',
        },
        spam_control={'contents': ['greetings', 'and salutations']},
        template_id=settings.CONTACT_FAS_COMPANY_NOTIFY_TEMPLATE_ID,
    )


@mock.patch.object(views.ContactCompanyView.form_class.action_class, 'save')
def test_contact_company_view_feature_submit_api_forms_failure(
    mock_save, client, valid_contact_company_data, retrieve_profile_data,
):
    mock_save.return_value = create_response(status_code=400)
    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        },
    )
    with pytest.raises(requests.exceptions.HTTPError):
        client.post(url, valid_contact_company_data)


@mock.patch.object(views.api_client.company, 'published_profile_retrieve', mock.Mock)
@mock.patch('core.helpers.get_company_profile')
def test_contact_company_exposes_context(mock_get_company_profile, client):
    mock_get_company_profile.return_value = data = {
        'number': '01234567',
        'slug': 'thing',
        'is_published_find_a_supplier': True,
        'company_type': 'COMPANIES_HOUSE',
    }
    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={'company_number': '01234567'}
    )

    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name == [views.ContactCompanyView.template_name]
    assert response.context_data['company'] == (
        CompanyParser(data).serialize_for_template()
    )


@mock.patch('find_a_supplier.views.CompanySearchView.get_results_and_count')
def test_company_search_submit_form_on_get(mock_get_results_and_count, client, search_results):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(reverse('find-a-supplier:search'), {'q': '123'})

    assert response.status_code == 200
    assert response.context_data['results'] == results


@pytest.mark.parametrize('params,expected', [
    ({'term': '123', 'sectors': 'AEROSPACE'}, 'q=123&industries=AEROSPACE'),
    ({'sectors': 'AEROSPACE'}, 'industries=AEROSPACE'),
    ({'term': '123'}, 'q=123'),
])
def test_company_search_redirects_using_old_params(client, params, expected):

    url = reverse('find-a-supplier:search')
    response = client.get(url, params)

    assert response.status_code == 302
    assert response.url == f'{url}?{expected}'


@mock.patch('find_a_supplier.views.CompanySearchView.get_results_and_count')
def test_company_search_pagination_count(mock_get_results_and_count, client, search_results):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(reverse('find-a-supplier:search'), {'q': '123'})

    assert response.status_code == 200
    assert response.context_data['pagination'].paginator.count == 20


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_search_pagination_param(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    url = reverse('find-a-supplier:search')
    response = client.get(
        url, {'q': '123', 'page': 1, 'industries': ['AEROSPACE']}
    )

    assert response.status_code == 200
    assert mock_search.call_count == 1
    assert mock_search.call_args == mock.call(
        page=1, size=10, term='123', sectors=['AEROSPACE'],
    )


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_search_sector_empty(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    url = reverse('find-a-supplier:search')
    response = client.get(
        url, {'q': '123', 'page': 1, 'industries': ''}
    )
    assert response.status_code == 200
    assert mock_search.call_count == 1
    assert mock_search.call_args == mock.call(
        page=1, size=10, term='123', sectors=[],
    )


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_search_pagination_empty_page(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    url = reverse('find-a-supplier:search')
    response = client.get(url, {'q': '123', 'page': 100})

    assert response.status_code == 302
    assert response.get('Location') == '/international/trade/search/?q=123'


@mock.patch('find_a_supplier.views.CompanySearchView.get_results_and_count')
def test_company_search_not_submit_without_params(
    mock_get_results_and_count, client
):
    response = client.get(reverse('find-a-supplier:search'))

    assert response.status_code == 200
    mock_get_results_and_count.assert_not_called()


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_search_api_call_error(mock_search, client):
    mock_search.return_value = create_response(status_code=400)

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(reverse('find-a-supplier:search'), {'q': '123'})


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
@mock.patch.object(views, 'get_results_from_search_response')
def test_company_search_api_success(mock_get_results_from_search_response, mock_search, client, search_results):
    mock_search.return_value = api_response = create_response(search_results)
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(reverse('find-a-supplier:search'), {'q': '123'})

    assert response.status_code == 200
    assert mock_get_results_from_search_response.call_count == 1
    assert mock_get_results_from_search_response.call_args == mock.call(api_response)


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_search_response_no_highlight(mock_search, client, search_results):
    mock_search.return_value = create_response(search_results)

    response = client.get(reverse('find-a-supplier:search'), {'q': 'wolf'})

    assert b'this is a short summary' in response.content


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_highlight_description(
    mock_search, search_results_description_highlight, client
):
    mock_search.return_value = create_response(search_results_description_highlight)

    response = client.get(reverse('find-a-supplier:search'), {'q': 'wolf'})
    expected = (
        b'<em>wolf</em> in sheep clothing description...'
        b'to the max <em>wolf</em>.'
    )

    assert expected in response.content


@mock.patch('directory_api_client.client.api_client.company.search_find_a_supplier')
def test_company_search_highlight_summary(
    mock_search, search_results_summary_highlight, client
):
    mock_search.return_value = create_response(search_results_summary_highlight)

    response = client.get(reverse('find-a-supplier:search'), {'q': 'wolf'})

    assert b'<em>wolf</em> in sheep clothing summary.' in response.content


@pytest.mark.parametrize('name,number,slug', [
    ['find-a-supplier:profile', '01234567',   'a'],
    ['find-a-supplier:profile', 'SC01234567', 'a'],
    ['find-a-supplier:profile-slugless', '01234567', None],
    ['find-a-supplier:profile-slugless', 'SC01234567', None],
    ['find-a-supplier:company-contact', '01234567', None],
    ['find-a-supplier:company-contact', 'SC01234567', None],
])
def test_company_profile_url_routing_200(name, number, slug):
    kwargs = {'company_number': number}
    if slug:
        kwargs['slug'] = slug

    assert reverse(name, kwargs=kwargs)


@pytest.mark.parametrize('name,number,slug', [
    ['find-a-supplier:profile',          '.', 'a'],
    ['find-a-supplier:profile-slugless', '.', None],
    ['find-a-supplier:company-contact', '.', 'a'],
])
def test_company_profile_url_routing_404(name, number, slug):
    kwargs = {'company_number': number}
    if slug:
        kwargs['slug'] = slug

    with pytest.raises(NoReverseMatch):
        assert reverse(name, kwargs=kwargs)


def test_contact_company_sent(client):
    url = reverse(
        'find-a-supplier:company-contact-sent',
        kwargs={'company_number': '01111111'}
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.ContactCompanySentView.template_name
    ]


@pytest.mark.parametrize('params', [
    {'show-guide': True},
    {'q': '', 'industries': ''},
    {'q': ''},
    {'industries': ''},
])
def test_home_page_show_guide(client, params):
    url = reverse('find-a-supplier:search')

    response = client.get(url, params)

    assert response.status_code == 200
    assert response.context_data['show_search_guide'] is True


@pytest.mark.parametrize('params', [
    {'q': 'foo', 'industries': 'bar'},
    {'q': 'bar'},
    {'industries': 'foo'},
    {}
])
@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_home_page_hide_guide(mock_get_results_and_count, client, params):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    url = reverse('find-a-supplier:search')

    response = client.get(url, params)

    assert response.status_code == 200
    assert response.context_data['show_search_guide'] is False


def test_anonymous_subscribe(client):
    response = client.get(reverse('find-a-supplier:subscribe'))

    assert response.status_code == 200


def test_anonymous_subscribe_success(client):
    response = client.get(reverse('find-a-supplier:subscribe-success'))

    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
@patch.object(views.IndustryLandingPageContactCMSView.form_class, 'save')
def test_industry_contact_submit_with_comment_forms_api(
    mock_save, mock_cms_page, client, captcha_stub, settings
):

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
        'page_type': 'InternationalTradeIndustryContactPage',
    }
    mock_cms_page.return_value = create_response(dummy_page)

    mock_save.return_value = create_response(status_code=200)

    url = reverse('find-a-supplier:industry-contact', kwargs={'path': 'trade/contact'})
    data = {
        'given_name': 'Jeff',
        'family_name': 'Goldblum',
        'email_address': 'jeff@example.com',
        'phone_number': '3223232',
        'sector': sectors.AEROSPACE,
        'organisation_name': 'My name is Jeff',
        'organisation_size': '1-10',
        'country': choices.COUNTRIES_AND_TERRITORIES[1][0],
        'body': 'hello',
        'source': constants.MARKETING_SOURCES[1][0],
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == (
        reverse('find-a-supplier:industry-contact-success', kwargs={'path': 'trade/contact'})
    )
    assert mock_save.call_count == 2
    assert mock_save.call_args_list[0] == call(
        email_address='buying@example.com',
        form_url='/international/trade/contact/',
        sender={
            'email_address': 'jeff@example.com',
            'country_code': choices.COUNTRIES_AND_TERRITORIES[1][0],
            'ip_address': '127.0.0.1'
        },
        spam_control={
            'contents': ['hello']},
        template_id=settings.CONTACT_INDUSTRY_AGENT_TEMPLATE_ID,
    )
    assert mock_save.call_args_list[1] == call(
        email_address='jeff@example.com',
        form_url='/international/trade/contact/',
        template_id=settings.CONTACT_INDUSTRY_USER_TEMPLATE_ID,
        email_reply_to_id=settings.CONTACT_INDUSTRY_USER_REPLY_TO_ID,
    )


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_industry_contact_sent_no_referer(mock_cms_page, client):

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
        'page_type': 'InternationalTradeIndustryContactPage',
    }
    mock_cms_page.return_value = create_response(dummy_page)

    url = reverse(
        'find-a-supplier:industry-contact-success', kwargs={'path': 'trade/contact'}
    )
    expected_url = reverse(
        'find-a-supplier:industry-contact', kwargs={'path': 'trade/contact'}
    )
    response = client.get(url, {})

    assert response.status_code == 302
    assert response.url == expected_url


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_industry_contact_sent_incorrect_referer(mock_cms_page, client):

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
        'page_type': 'InternationalTradeIndustryContactPage',
    }
    mock_cms_page.return_value = create_response(dummy_page)

    url = reverse(
        'find-a-supplier:industry-contact-success', kwargs={'path': 'trade/contact'}
    )
    expected_url = reverse(
        'find-a-supplier:industry-contact', kwargs={'path': 'trade/contact'}
    )
    referer_url = 'http://www.googe.com'
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 302
    assert response.url == expected_url


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_industry_contact_sent_correct_referer(mock_cms_page, client):

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
        'page_type': 'InternationalTradeIndustryContactPage',
    }
    mock_cms_page.return_value = create_response(dummy_page)

    url = reverse(
        'find-a-supplier:industry-contact-success', kwargs={'path': 'trade/contact'}
    )
    referer_url = reverse(
        'find-a-supplier:industry-contact', kwargs={'path': 'trade/contact'}
    )
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 200
    assert response.template_name == [
        views.IndustryLandingPageContactCMSSuccessView.template_name
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_industry_contact_has_privacy_url(mock_cms_page, client):

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
        'page_type': 'InternationalTradeIndustryContactPage',
    }
    mock_cms_page.return_value = create_response(dummy_page)

    url = reverse(
        'find-a-supplier:industry-contact', kwargs={'path': 'trade/contact'}
    )
    response = client.get(url, {})
    assert response.status_code == 200
    assert response.context_data['privacy_url']


@mock.patch('directory_forms_api_client.client.forms_api_client.submit_generic')
def test_industry_contact_serialized_data(mock_submit_generic, valid_contact_data):
    mock_submit_generic.return_value = None
    form = forms.BuyFromTheUKForm(data=valid_contact_data)
    data = valid_contact_data

    assert form.is_valid()

    form.save(
        template_id='foo',
        email_address='reply_to@example.com',
        form_url='/trade/some/path/',
    )

    assert form.serialized_data == {
        'given_name': data['given_name'],
        'family_name': data['family_name'],
        'email_address': data['email_address'],
        'email_contact_consent': data['email_contact_consent'],
        'telephone_contact_consent': data['telephone_contact_consent'],
        'phone_number': data['phone_number'],
        'sector': data['sector'],
        'organisation_name': data['organisation_name'],
        'organisation_size': choices.EMPLOYEES[0][1],
        'country': choices.COUNTRIES_AND_TERRITORIES[0][0],
        'country_name': choices.COUNTRIES_AND_TERRITORIES[0][1],
        'body': data['body'],
        'source': data['source'],
        'source_other': '',
    }


def test_unsubscribe_required_params(client):
    response = client.get(reverse('find-a-supplier:unsubscribe'), {'email': '123'})

    assert response.status_code == 200
    assert response.template_name == [views.UnsubscribeView.template_name]


def test_unsubscribe_missing_required_params(client):
    response = client.get(reverse('find-a-supplier:unsubscribe'))

    assert response.status_code == 302
    assert response.url == reverse('find-a-supplier:trade-home')


@patch.object(views.api_client.notifications, 'anonymous_unsubscribe')
def test_unsubscribe_api_validation_failure(mock_unsubscribe, client):
    mock_unsubscribe.return_value = create_response(status_code=400)

    response = client.post(reverse('find-a-supplier:unsubscribe'), {'email': '123'})

    assert response.status_code == 200
    assert response.template_name == views.UnsubscribeView.failure_template_name


@patch.object(views.api_client.notifications, 'anonymous_unsubscribe')
def test_unsubscribe_api_error(mock_unsubscribe, client):
    mock_unsubscribe.return_value = create_response(status_code=500)

    with pytest.raises(requests.exceptions.HTTPError):
        client.post(reverse('find-a-supplier:unsubscribe'), {'email': '123'})


@patch.object(views.api_client.notifications, 'anonymous_unsubscribe')
def test_unsubscribe_api_success(mock_unsubscribe, client):
    mock_unsubscribe.return_value = create_response()

    response = client.post(reverse('find-a-supplier:unsubscribe'), {'email': '123'})

    mock_unsubscribe.assert_called_once_with('123')
    assert response.status_code == 200
    assert response.template_name == views.UnsubscribeView.success_template_name
