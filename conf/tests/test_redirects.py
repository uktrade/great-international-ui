from unittest import mock
import pytest

from django.urls import reverse


# the first element needs to end with a slash
redirects = [
    (
        '/international/eu-exit-news/contact/',
        reverse('brexit-international-contact-form'),
    ),
    (
        '/international/eu-exit-news/contact/success/',
        reverse('brexit-international-contact-form-success'),
    ),
    (
        '/international/brexit/contact/',
        reverse('brexit-international-contact-form'),
    ),
    (
        '/international/brexit/contact/success/',
        reverse('brexit-international-contact-form-success'),
    ),
    (
        '/international/content/opportunities/',
        '/international/investment/opportunities/'
    ),
    (
        '/international/content/opportunities/?Region=Wales&Sector=Test',
        '/international/investment/opportunities/?Region=Wales&Sector=Test'
    ),
    (
        '/international/content/invest/high-potential-opportunities/contact/',
        '/international/content/investment/foreign-direct-investment-contact/'
    ),
    (
        '/international/content/invest/high-potential-opportunities/contact/success/',
        '/international/content/investment/foreign-direct-investment-contact/success/'
    ),
    (
        '/international/content/expand/high-potential-opportunities/contact/',
        '/international/content/investment/foreign-direct-investment-contact/'
    ),
    (
        '/international/content/expand/high-potential-opportunities/contact/success/',
        '/international/content/investment/foreign-direct-investment-contact/success/',
    ),
    (
        '/international/invest/',
        '/international/investment/',
    ),
    (
        '/international/content/invest/test/',
        '/international/investment/',  # just all sent to the atlas root
    ),
    (
        '/international/content/opportunities/',
        '/international/investment/opportunities/',
    ),
    (
        '/international/content/opportunities/test-opp-here/',
        '/international/investment/opportunities/',
    ),
    (
        '/international/content/invest/high-potential-opportunities',
        '/international/investment/opportunities/',
    ),
    (
        '/international/content/invest/high-potential-opportunities/test/',
        '/international/investment/opportunities/',
    ),

    # About the UK was moved over to Why Invest in the UK
    (
        '/international/content/about-uk/',
        '/international/content/investment/why-invest-in-the-uk/',
    ),
    (
        '/international/content/about-uk/why-choose-uk/',
        '/international/content/investment/why-invest-in-the-uk/',
    ),
    (
        '/international/content/about-uk/why-choose-uk/tax-incentives/',
        '/international/content/investment/why-invest-in-the-uk/tax-incentives/',
    ),
    (
        '/international/content/about-uk/why-choose-uk/uk-talent-and-labour/',
        '/international/content/investment/why-invest-in-the-uk/uk-talent-and-labour/',
    ),
    (
        '/international/content/about-uk/why-choose-uk/uk-innovation/',
        '/international/content/investment/why-invest-in-the-uk/uk-innovation/',
    ),
    (

        '/international/content/about-uk/why-choose-uk/uk-infrastructure/',
        '/international/content/investment/why-invest-in-the-uk/uk-infrastructure/',
    ),
    (
        '/international/content/about-uk/industries/',
        '/international/content/investment/sectors/',
    )
]


@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)
    assert response.url == expected


not_redirected = (
    '/international/invest/perfectfit/',  # needs PIR API call mocked

    # This form is kept in place during atlas refactor - can be moved later
    '/international/invest/contact/',
    '/international/invest/contact/success/',
    '/international/expand/contact/',
    '/international/expand/contact/success/',
)


@mock.patch('pir_client.client.pir_api_client.get_options')
@pytest.mark.parametrize('url', not_redirected)
def test_does_NOT_redirect(mock_get_options, url, client):
    response = client.get(url)
    assert response.status_code == 200  # not 30x
    assert not hasattr(response, 'url')
