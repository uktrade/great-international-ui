import pytest
from django.urls import reverse


@pytest.mark.parametrize('source,destination', [
    ('', '/international/trade/'),
    ('industries/contact', '/international/trade/contact/'),
    ('search', '/international/trade/search/'),
    ('industries', '/international/content/industries/'),
    ('industries/creative-services', '/international/content/industries/creative-industries/'),
    ('industries/energy', '/international/content/industries/nuclear-energy/'),
    ('industries/healthcare', '/international/content/industries/health-and-life-sciences/'),
    ('industries/innovation-industry', '/international/content/industries/technology/'),
    ('industries/life-sciences', '/international/content/industries/health-and-life-sciences/'),
    ('industries/professional-and-financial-services', '/international/content/industries/financial-services/'),
    ('industries/sports-economy', '/international/content/industries/sports-economy/'),
    ('industries/technology', '/international/content/industries/technology/'),
    ('industries/aerospace', '/international/content/industries/aerospace/'),
    ('industries/agricultural-technology', '/international/content/industries/agricultural-technology/'),
    ('industries/automotive', '/international/content/industries/automotive/'),
    ('industries/business-and-government-partnerships', '/international/content/industries/'),
    ('industries/consumer-retail', '/international/content/industries/retail/'),
    ('industries/cyber-security', '/international/content/industries/cyber-security/'),
    ('industries/education-industry', '/international/content/industries/education/'),
    ('industries/engineering-industry', '/international/content/industries/engineering-and-manufacturing/'),
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
     '/international/content/industries/engineering-and-manufacturing/global-rail-experience/'),
    ('industry-articles/established-mining-industry-article/',
     '/international/content/industries/engineering-and-manufacturing/established-mining-industry/'),
    ('industry-articles/trusted-construction-partners-article/',
     '/international/content/industries/engineering-and-manufacturing/trusted-construction-partners/'),
    ('industry-articles/how-tech-is-changing-the-way-we-bank-article/',
     '/international/content/industries/financial-services/how-tech-is-changing-the-way-we-bank/'),
    ('industry-articles/a-global-centre-for-life-sciences/',
     '/international/content/industries/health-and-life-sciences/a-global-centre-for-life-sciences/'),
    ('industry-articles/building-fintech-bridges-article/',
     '/international/content/industries/financial-services/building-fintech-bridges/'),
    ('industry-articles/a-focus-on-regulatory-technology-solutions-article/',
     '/international/content/industries/financial-services/a-focus-on-regulatory-technology-solutions/'),
    ('industries/infrastructure/', '/international/content/industries/infrastructure/'),
    ('unsubscribe', '/international/trade/unsubscribe/'),
])
def test_supplier_redirects(source, destination, client):
    url = reverse('trade-incoming', kwargs={'path': source})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == destination


@pytest.mark.parametrize('url,destination', (
    ('/trade/industries/healthcare/', '/international/content/industries/health-and-life-sciences/'),
    ('/trade/industries/life-sciences/', '/international/content/industries/health-and-life-sciences/'),
    ('/trade/industries/engineering-industry/', '/international/content/industries/engineering-and-manufacturing/'),
))
def test_industries_incoming(url, destination, client):
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == destination
