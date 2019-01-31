from importlib import import_module
from unittest.mock import call, patch

from directory_constants.constants import choices
import pytest
from requests.exceptions import HTTPError

from django.urls import reverse

from core.tests.helpers import create_response
from opportunities import views


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_payload={'opportunity_list': []}
    )

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.HighPotentialOpportunityFormView.template_name
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_not_found(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )
    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_cms_retrieval_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'full_name': {
                'help_text': 'full name help text'
            },
            'role_in_company': {
                'help_text': 'role help text'
            },
            'opportunity_list': [
                {
                    'pdf_document': 'http://www.example.com/a',
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail'}
                }
            ]
        }
    )

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['full_name'].help_text == 'full name help text'
    assert form.fields['role_in_company'].help_text == 'role help text'
    assert form.fields['opportunities'].choices == [
        ('http://www.example.com/a', 'some great opportunity'),
    ]
    assert form.initial['opportunities'] == ['http://www.example.com/a']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_cms_retrieval_not_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=400)

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    with pytest.raises(HTTPError):
        client.get(url)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'meta': {'languages': [['en-gb', 'English']]}
        }
    )

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.HighPotentialOpportunityDetailView.template_name
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail_not_found(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail_cms_retrieval_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'title': '1234',
            'meta': {'languages': [['en-gb', 'English']]},
        }
    )

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page'] == {
        'title': '1234', 'meta': {'languages': [['en-gb', 'English']]}}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail_cms_retrieval_not_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=400)

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    with pytest.raises(HTTPError):
        client.get(url)


@patch('opportunities.forms.HighPotentialOpportunityForm.action_class')
@patch('opportunities.forms.HighPotentialOpportunityForm.action_class.save')
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_submmit_cms_retrieval_ok(
    mock_lookup_by_slug, mock_save, mock_action_class, settings, client,
    captcha_stub
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_payload={
            'opportunity_list': [
                {
                    'pdf_document': 'http://www.example.com/a',
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail'}
                }
            ]
        }
    )
    mock_save.return_value = create_response(status_code=200)
    settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS = 'invest@example.com'

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.post(url, {
        'full_name': 'Jim Example',
        'role_in_company': 'Chief chief',
        'email_address': 'test@example.com',
        'phone_number': '555',
        'company_name': 'Example corp',
        'website_url': 'example.com',
        'country': choices.COUNTRY_CHOICES[1][0],
        'company_size': '1 - 10',
        'opportunities': [
            'http://www.example.com/a',
        ],
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'high-potential-opportunity-request-form-success',
        kwargs={'slug': 'rail'}
    )

    assert mock_action_class.call_args_list[0] == call(
        email_address=settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS,
        template_id=settings.HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID,
        form_url=url,
    )
    assert mock_action_class.call_args_list[1] == call(
        email_address='test@example.com',
        template_id=settings.HPO_GOV_NOTIFY_USER_TEMPLATE_ID,
        form_url=url,
    )


def test_get_success_page_no_session(client, settings):

    url = reverse(
        'high-potential-opportunity-request-form-success',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_success_page_with_session(
    mock_lookup_by_slug, settings, client
):

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

    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_payload={
            'opportunity_list': [
                {
                    'pdf_document': 'http://www.example.com/a',
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail'}
                },
                {
                    'pdf_document': 'http://www.example.com/b',
                    'heading': 'some other opportunity',
                    'meta': {'slug': 'other'}
                }
            ],
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
        }
    )

    url = reverse(
        'high-potential-opportunity-request-form-success',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page']
    assert response.context_data['opportunities'] == [
        {
            'pdf_document': 'http://www.example.com/a',
            'heading': 'some great opportunity',
            'meta': {'slug': 'rail'}
        }
    ]
