import pytest

from unittest.mock import patch

from django.core.urlresolvers import reverse

from find_a_supplier.forms import SearchForm
from core.tests.helpers import create_response, stub_page



@pytest.fixture
def fas_home_page():
    yield from stub_page({
        'page_type': 'InternationalTradeHomePage',
    })


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_fas_homepage_search_form(mock_cms_response, fas_home_page, client):
    mock_cms_response.return_value = create_response(
        status_code=200,
        json_payload=fas_home_page.return_value.json()
    )

    url = reverse('trade-home')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['search_form'] == SearchForm


@pytest.mark.parametrize('source,destination', [
    ('', '/international/trade/'),
    ('industries/contact', '/international/trade/industries/contact/'),
    ('search', '/international/trade/search/'),
    ('industries', '/international/content/industries'),
    ('industries/creative-services', '/international/content/industries/creative-industries'),
    ('industries/energy', '/international/content/industries/nuclear-energy/'),
    ('industries/healthcare', '/international/content/industries/healthcare-and-life-sciences/'),
    ('industries/innovation-industry', '/international/content/industries/technology/'),
    ('industries/life-sciences', '/international/content/industries/healthcare-and-life-sciences/'),
    ('industries/professional-and-financial-services', '/international/content/industries/financial-services'),
    ('industries/sports-economy', '/international/content/industries/sports-economy/'),
    ('industries/technology', '/international/content/industries/technology'),
    ('industries/aerospace', '/international/content/industries/aerospace/'),
    ('industries/agricultural-technology', '/international/content/industries/agricultural-technology/'),
    ('industries/automotive', '/international/content/industries/automotive'),
    ('industries/business-and-government-partnerships', '/international/content/industries'),
    ('industries/consumer-retail', '/international/content/industries/retail/'),
    ('industries/cyber-security', '/international/content/industries/cyber-security/'),
    ('industries/education-industry', '/international/content/industries/education/'),
    ('industries/engineering-industry', '/international/content/industries/advanced-manufacturing/'),
    ('industries/food-and-drink', '/international/content/industries/food-and-drink/'),
    ('industries/legal-services', '/international/content/industries/legal-services/'),
    ('industries/marine', '/international/content/industries/maritime/'),
    ('industries/space/', '/international/content/industries/space/'),
    ('industry-articles/UK-agritech-strengths-article/', '/international/content/industries/agricultural-technology/'),
    ('industry-articles/global-humanitarian-support-article/', '/international/content/industries/'),
    ('industry-articles/uk-centres-of-excellence/',
     '/international/content/industries/retail/uk-centres-of-excellence/'),
    ('industry-articles/the-changing-face-of-visual-effects/',
     '/international/content/industries/creative-industries/the-changing-face-of-visual-effects/'),
    ('industry-articles/how-education-is-going-digital/',
     '/international/content/industries/education/how-education-is-going-digital/'),
    ('industry-articles/world-class-research-centre-article/',
     '/international/content/industries/nuclear-energy/world-class-research-centre/'),
    ('industry-articles/home-of-oil-and-gas-innovation-article/',
     '/international/content/industries/oil-and-gas/home-of-oil-and-gas-innovation/'),
    ('industry-articles/leading-the-world-in-cancer-care/',
     '/international/content/industries/health-and-life-sciences/leading-the-world-in-cancer-care/'),
    ('industry-articles/highly-rated-primary-care/',
     '/international/content/industries/health-and-life-sciences/highly-rated-primary-care/'),
    ('industry-articles/helping-you-buy-from-the-uk-article-ukef/',
     '/international/content/industries/infrastructure/helping-you-buy-from-the-uk-article-ukef/'),
    ('industry-articles/global-rail-experience-article/',
     '/international/content/industries/advanced-manufacturing/global-rail-experience/'),
    ('industry-articles/established-mining-industry-article/',
     '/international/content/industries/advanced-manufacturing/established-mining-industry'),
    ('industry-articles/trusted-construction-partners-article/',
     '/international/content/industries/advanced-manufacturing/trusted-construction-partners/'),
    ('industry-articles/how-tech-is-changing-the-way-we-bank-article/',
     '/international/content/industries/financial-services/how-tech-is-changing-the-way-we-bank/'),
    ('industry-articles/a-global-centre-for-life-sciences/',
     '/international/content/industries/health-and-life-sciences/a-global-centre-for-life-sciences/'),
    ('industry-articles/building-fintech-bridges-article/',
     '/international/content/industries/financial-services/building-fintech-bridges/'),
    ('industry-articles/a-focus-on-regulatory-technology-solutions-article/',
     '/international/content/industries/financial-services/a-focus-on-regulatory-technology-solutions/'),
    ('industries/infrastructure/', '/international/content/industries/infrastructure')
])
def test_supplier_redirects(source, destination, client):
    url = reverse('trade-incoming', kwargs={'path': source})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == destination


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
