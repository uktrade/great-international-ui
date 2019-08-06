import pytest
from unittest.mock import call, patch
from importlib import import_module
from requests.exceptions import HTTPError
from django.urls import reverse

from directory_constants import choices

from core.tests.helpers import create_response
from invest import views


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'meta': {'languages': [['en-gb', 'English']]},
            'page_type': 'InvestHighPotentialOpportunityDetailPage',
        }
    )

    url = '/international/content/invest/high-potential-opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'invest/hpo/high_potential_opportunity_detail.html'
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail_not_found(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(status_code=404)

    url = '/international/content/invest/high-potential-opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail_cms_retrieval_ok(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(
        status_code=200, json_payload={
            'title': '1234',
            'meta': {'languages': [['en-gb', 'English']]},
            'page_type': 'InvestHighPotentialOpportunityDetailPage',
        }
    )

    url = '/international/content/invest/high-potential-opportunities/rail/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page'] == {
        'title': '1234', 'meta': {'languages': [['en-gb', 'English']]},
        'page_type': 'InvestHighPotentialOpportunityDetailPage',
    }


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_detail_cms_retrieval_not_ok(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(status_code=400)

    url = '/international/content/invest/high-potential-opportunities/rail/'

    with pytest.raises(HTTPError):
        client.get(url)


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_form(mock_lookup_by_path, settings, client):
    mock_lookup_by_path.return_value = create_response(
        status_code=200,
        json_payload={
            'opportunity_list': [],
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InvestHighPotentialOpportunityFormPage',
        }
    )

    url = reverse('high-potential-opportunity-request-form')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.HighPotentialOpportunityFormView.template_name
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_form_not_found(mock_lookup_by_path, settings, client):
    mock_lookup_by_path.return_value = create_response(status_code=404)

    url = reverse('high-potential-opportunity-request-form')
    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_form_cms_retrieval_ok(mock_lookup_by_path, settings, client):
    mock_lookup_by_path.return_value = create_response(
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
            ],
            'page_type': 'InvestHighPotentialOpportunityFormPage',
        }
    )

    url = reverse('high-potential-opportunity-request-form')

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['full_name'].help_text == 'full name help text'
    assert form.fields['role_in_company'].help_text == 'role help text'
    assert form.fields['opportunities'].choices == [
        ('http://www.example.com/a', 'some great opportunity'),
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_form_cms_retrieval_not_ok(
    mock_lookup_by_path, settings, client
):
    mock_lookup_by_path.return_value = create_response(status_code=400)

    url = reverse('high-potential-opportunity-request-form')

    with pytest.raises(HTTPError):
        client.get(url)


@patch('invest.forms.HighPotentialOpportunityForm.action_class')
@patch('invest.forms.HighPotentialOpportunityForm.action_class.save')
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_high_potential_opportunity_form_submmit_cms_retrieval_ok(
    mock_lookup_by_path, mock_save, mock_action_class, settings, rf,
    captcha_stub
):
    mock_lookup_by_path.return_value = create_response(
        status_code=200,
        json_payload={
            'opportunity_list': [
                {
                    'pdf_document': 'http://www.example.com/a',
                    'heading': 'some great opportunity',
                    'meta': {'slug': 'rail'}
                }
            ],
            'page_type': 'InvestHighPotentialOpportunityFormPage',
        }
    )
    mock_save.return_value = create_response(status_code=200)
    settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS = 'invest@example.com'

    url = reverse('high-potential-opportunity-request-form')

    request = rf.post(url, data={
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

    utm_data = {
        'campaign_source': 'test_source',
        'campaign_medium': 'test_medium',
        'campaign_name': 'test_campaign',
        'campaign_term': 'test_term',
        'campaign_content': 'test_content'
    }
    request.utm = utm_data
    request.session = {}
    response = views.HighPotentialOpportunityFormView.as_view()(
        request,
        path='/invest/high-potential-opportunities/contact/success/',
    )

    assert response.status_code == 302
    assert response.url == reverse('high-potential-opportunity-request-form-success')

    assert mock_action_class.call_args_list[0] == call(
        email_address=settings.HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS,
        template_id=settings.HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID,
        form_url=url,
        sender={'email_address': 'test@example.com', 'country_code': 'AL'}
    )
    assert mock_action_class.call_args_list[1] == call(
        email_address='test@example.com',
        template_id=settings.HPO_GOV_NOTIFY_USER_TEMPLATE_ID,
        form_url=url,
        email_reply_to_id=settings.HPO_GOV_NOTIFY_USER_REPLY_TO_ID,
    )


def test_get_success_page_no_session(client, settings):

    url = reverse('high-potential-opportunity-request-form-success')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('high-potential-opportunity-request-form')


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_get_success_page_with_session(
    mock_lookup_by_path, settings, client
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

    mock_lookup_by_path.return_value = create_response(
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
            'page_type': 'InvestHighPotentialOpportunityFormSuccessPage',
        }
    )

    url = reverse('high-potential-opportunity-request-form-success')

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


@pytest.mark.parametrize('source,destination', [
    (
        'high-potential-opportunities/rail-infrastructure',
        '/international/content/invest/high-potential-opportunities/rail-infrastructure/'
    ),
    (
        'high-potential-opportunities/food-production',
        '/international/content/invest/high-potential-opportunities/food-production/'
    ),
    (
        'high-potential-opportunities/lightweight-structures',
        '/international/content/invest/high-potential-opportunities/lightweight-structures/'
    ),
    (
        'high-potential-opportunities/rail-infrastructure/contact',
        '/international/content/invest/high-potential-opportunities/rail-infrastructure/contact/'
    ),
    (
        'high-potential-opportunities/food-production/contact',
        '/international/content/invest/high-potential-opportunities/food-production/contact/'
    ),
    (
        'high-potential-opportunities/lightweight-structures/contact',
        '/international/content/invest/high-potential-opportunities/lightweight-structures/contact/'
    ),
])
def test_invest_redirects(source, destination, client):
    url = reverse('invest-incoming', kwargs={'path': source})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == destination


@pytest.mark.parametrize('source,destination', [
    (
        '/es/industries/',
        '/international/content/industries/?lang=es'
    ),
    (
        '/de/industries/',
        '/international/content/industries/?lang=de'
    ),
    (
        '/fr/industries/',
        '/international/content/industries/?lang=fr'
    ),
    (
        '/pt/industries/',
        '/international/content/industries/?lang=pt'
    ),
    (
        '/zh-hans/industries/',
        '/international/content/industries/?lang=zh-hans'
    ),
    (
        '/ar/industries/',
        '/international/content/industries/'
    ),
    (
        '/ja/industries/',
        '/international/content/industries/'
    ),
])
def test_invest_redirects_language_urls(source, destination, client):
    url = reverse('invest-incoming', kwargs={'path': source})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == destination


def test_invest_redirects_persist_querystrings(client):
    url = reverse('invest-incoming', kwargs={'path': '/es/industries/'})
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/content/industries/?foo=bar&lang=es'


def test_invest_redirect_homepage(client):
    url = reverse('invest-incoming', kwargs={'path': '/es/'})
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/invest/?foo=bar&lang=es'


def test_invest_redirect_homepage_english(client):
    url = reverse('invest-incoming-homepage')
    response = client.get(url, {'foo': 'bar'})
    assert response.status_code == 302
    assert response.url == '/international/invest/?foo=bar'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_uk_region_page_cms_view(mock_get_page, client):
    mock_get_page.return_value = create_response(
        status_code=200,
        json_payload={
            'meta': {
                'languages': [['en-gb', 'English']],
                'slug': 'region-slug',
            },
            'page_type': 'InvestRegionPage',
        }
    )

    url = reverse('cms-page-from-path', kwargs={'path': '/invest/uk-regions/region-slug'})
    response = client.get(url)

    assert response.status_code == 200
