import pytest

from django.urls import reverse


# the first element needs to end with a slash
redirects = [
    ('/international/eu-exit-news/contact/', reverse('brexit-international-contact-form')),
    ('/international/eu-exit-news/contact/success/', reverse('brexit-international-contact-form-success')),
    ('/international/content/industries/advanced-manufacturing/', '/international/content/industries/engineering-and-manufacturing/'),  # NOQA
    ('/international/content/about-uk/industries/advanced-manufacturing/', '/international/content/about-uk/industries/engineering-and-manufacturing/'),  # NOQA
]
@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)
    assert response.url == expected
