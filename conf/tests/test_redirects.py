from unittest import mock
import pytest

from core.tests.helpers import create_response

# the first element needs to end with a slash
redirects = [
    (
        '/international/trade/investment-support-directory/search/',
        '/international/investment-support-directory/'
    ),
    (
        '/international/content/trade/',
        '/international/trade/'
    ),
    (
        '/international/content/trade/contact/',
        '/international/trade/contact/'
    ),
    (
        '/international/trade/incoming/',
        '/international/trade/'
    ),
    (
        '/international/content/invest/',
        '/international/investment/'
    ),
    (
        '/international/invest/incoming/',
        '/international/investment/'
    ),
    (
        '/international/invest/incoming/foo/',
        '/international/investment/'
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
        '/international/content/expand/',
        '/international/investment/'
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
        '/international/content/invest/high-potential-opportunities/',
        '/international/investment/opportunities/',
    ),
    (
        '/international/content/invest/high-potential-opportunities/test/',
        '/international/investment/opportunities/',
    ),
    (
        '/international/content/investment/opportunities/',
        '/international/investment/opportunities/'
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

        '/international/content/about-uk/why-choose-uk/uk-infrastructure//',
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
        '/international/content/how-to-setup-in-the-uk/',
        '/international/content/invest/how-to-setup-in-the-uk/'
    ),
    (
        '/international/content/invest/how-to-setup-in-the-uk/',
        '/international/investment/'
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
    (
        '/international/content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk//',
        '/international/content/investment/how-we-can-help/access-finance-in-the-uk/',
    ),

]


@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)
    assert response.url == expected


not_redirected = (
    '/international/investment-support-directory/',
    # just a light check of SOME but not all views
    '/international/invest/contact/',
    '/international/invest/contact/success/',
    '/international/expand/contact/',
    '/international/expand/contact/success/',
)


@pytest.mark.parametrize('url', not_redirected)
@mock.patch('pir_client.client.pir_api_client.get_options')
def test_does_not_redirect(
        mock_get_options,
        url,
        client,
):
    response = client.get(url)
    assert response.status_code == 200  # not 30x
    assert not hasattr(response, 'url')


not_redirected_cms = (
    ('/international/trade/', 'InternationalTradeHomePage'),
)


@pytest.mark.parametrize('url,page_type', not_redirected_cms)
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_does_not_redirect_cms_pages(mock_lookup_by_path, url, page_type, client):
    mock_lookup_by_path.return_value = create_response(
        status_code=200,
        json_payload={
            'title': url,
            'meta': {
                'languages': [
                    ['en-gb', 'English'],
                ]
            },
            'page_type': page_type,
        }
    )
    response = client.get(url)
    assert response.status_code == 200  # not 30x
    assert not hasattr(response, 'url')
