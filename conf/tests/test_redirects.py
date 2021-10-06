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
        '/international/content/capital-invest/',
        '/international/investment/',
    ),
    (
        '/international/content/capital-invest/how-we-help-you-invest-capital/',
        '/international/content/investment/how-we-can-help/',
    ),
    (
        '/international/content/invest/test/',
        '/international/investment/',  # just all sent to the atlas root
    ),
    (
        '/international/content/about-us/',
        '/international/content/investment/how-we-can-help/',
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
    ),
    (
        '/international/content/about-uk/regions/',
        '/international/content/investment/regions/',
    ),
    (
        '/international/content/about-uk/regions/scotland/',
        '/international/content/investment/regions/scotland/',
    ),
    (
        '/international/content/about-uk/regions/northern-ireland/',
        '/international/content/investment/regions/northern-ireland/',
    ),
    (
        '/international/content/about-uk/regions/north-england/',
        '/international/content/investment/regions/north-england/',
    ),
    (
        '/international/content/about-uk/regions/wales/',
        '/international/content/investment/regions/wales/',
    ),
    (
        '/international/content/about-uk/regions/midlands/',
        '/international/content/investment/regions/midlands/',
    ),
    (
        '/international/content/about-uk/regions/south-england/',
        '/international/content/investment/regions/south-england/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/',
        '/international/content/investment/how-we-can-help/establish-a-base-for-business-in-the-uk/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/',
        '/international/content/investment/how-we-can-help/research-and-development-rd-support-in-the-uk/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/global-entrepreneur-program/',
        '/international/content/investment/how-we-can-help/global-entrepreneur-program/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/uk-visas-and-migration/',
        '/international/content/investment/how-we-can-help/uk-visas-and-migration/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/register-a-company-in-the-uk/',
        '/international/content/investment/how-we-can-help/register-a-company-in-the-uk/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/',
        '/international/content/investment/how-we-can-help/hire-skilled-workers-for-your-uk-operations/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/',
        '/international/content/investment/how-we-can-help/open-a-uk-business-bank-account/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/uk-tax-and-incentives/',
        '/international/content/investment/how-we-can-help/uk-tax-and-incentives/',
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/',
        '/international/content/investment/how-we-can-help/access-finance-in-the-uk/',
    ),

]


@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)
    assert response.url == expected


not_redirected = (
    '/international/invest/perfectfit/',  # needs PIR API call mocked

    # just a light check of SOME but not all views
    '/international/contact/',
    '/international/invest/contact/',
    '/international/invest/contact/success/',
    '/international/expand/contact/',
    '/international/expand/contact/success/',
    '/international/transition-period/contact/',
)


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_path')
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch('pir_client.client.pir_api_client.get_options')
@pytest.mark.parametrize('url', not_redirected)
def test_does_NOT_redirect(
        mock_lookup_by_path,
        mock_lookup_by_slug,
        mock_get_options,
        url,
        client,
):
    response = client.get(url)
    assert response.status_code == 200  # not 30x
    assert not hasattr(response, 'url')
