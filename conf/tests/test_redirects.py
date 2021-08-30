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
    )
]


@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)
    assert response.url == expected
