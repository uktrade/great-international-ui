from unittest import mock

from directory_constants import choices
from django.urls import reverse

from core.tests.helpers import create_response
from euexit import views


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_form(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'disclaimer': 'disclaim',
            'page_type': 'InternationalEUExitFormPage'
        }
    )

    response = client.get(reverse('eu-exit-international-contact-form'))

    assert response.status_code == 200
    assert response.template_name == [
        views.InternationalContactFormView.template_name
    ]


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_form_not_found(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    url = reverse('eu-exit-international-contact-form')
    response = client.get(url)

    assert response.status_code == 404


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_form_cms_retrieval_ok(
        mock_lookup_by_slug, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'first_name': {
                'label': 'Given name'
            },
            'last_name': {
                'label': 'Family name'
            },
            'disclaimer': 'disclaim',
            'page_type': 'InternationalEUExitFormPage'
        }
    )
    url = reverse('eu-exit-international-contact-form')
    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['first_name'].label == 'Given name'
    assert form.fields['last_name'].label == 'Family name'
    assert form.fields['terms_agreed'].widget.label.endswith('disclaim')


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(
    views.InternationalContactFormView.form_class, 'save'
)
def test_international_form_submit(
        mock_save, mock_lookup_by_slug, settings, client, captcha_stub
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'disclaimer': 'disclaim',
            'page_type': 'InternationalEUExitFormPage'
        }
    )
    settings.EU_EXIT_ZENDESK_SUBDOMAIN = 'eu-exit-subdomain'

    url = reverse('eu-exit-international-contact-form')

    # sets referrer in the session
    client.get(url, {}, HTTP_REFERER='http://www.google.com')
    response = client.post(url, {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRY_CHOICES[1][0],
        'city': 'London',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'eu-exit-international-contact-form-success'
    )
    assert mock_save.call_count == 1
    assert mock_save.call_args == mock.call(
        subject='EU exit international contact form',
        full_name='test example',
        email_address='test@example.com',
        service_name='eu_exit',
        subdomain=settings.EU_EXIT_ZENDESK_SUBDOMAIN,
        form_url=url,
        sender={'email_address': 'test@example.com', 'country_code': None}
    )


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_success_page(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_payload={
            'body_text': 'what next',
            'disclaimer': 'disclaim',
            'page_type': 'InternationalEUExitFormSuccessPage'
        }
    )
    url = reverse('eu-exit-international-contact-form-success')
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.InternationalContactSuccessView.template_name
    ]
    assert response.context_data['page'] == {
        'body_text': 'what next',
        'disclaimer': 'disclaim',
        'page_type': 'InternationalEUExitFormSuccessPage'
    }


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_urls(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_payload={
            'disclaimer': 'disclaim',
            'page_type': 'InternationalEUExitFormPage'
        }
    )
    url = reverse('eu-exit-international-contact-form')
    response = client.get(url, {}, HTTP_REFERER='http://www.google.com')

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['terms_agreed'].widget.label.endswith('disclaim')
    assert form.ingress_url == 'http://www.google.com'


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_urls_no_referer(mock_lookup_by_slug, client):
    url = reverse('eu-exit-international-contact-form')
    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_payload={
            'disclaimer': 'disclaim',
            'page_type': 'InternationalEUExitFormPage'
        }
    )

    response = client.get(url, {})
    assert response.status_code == 200
    form = response.context_data['form']
    assert form.ingress_url is None
