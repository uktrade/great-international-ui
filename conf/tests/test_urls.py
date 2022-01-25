from importlib import import_module, reload
import sys

import pytest

from django.urls import clear_url_caches, reverse
from django.urls.exceptions import NoReverseMatch


def reload_urlconf(settings):
    clear_url_caches()
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    else:
        import_module(settings.ROOT_URLCONF)


def test_url_redirect_how_set_up_invest_page_on(client, settings):
    settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON'] = True
    reload_urlconf(settings)

    response = client.get('/international/content/how-to-setup-in-the-uk/')
    assert response.status_code == 302
    assert response.url == '/international/content/invest/how-to-setup-in-the-uk/'

    response = client.get('/international/content/how-to-setup-in-the-uk/some-set-up-guide/')
    assert response.status_code == 302
    assert response.url == '/international/content/invest/how-to-setup-in-the-uk/some-set-up-guide'


def test_url_redirect_how_set_up_redirect_off(client, settings):
    settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON'] = False
    reload_urlconf(settings)

    with pytest.raises(NoReverseMatch):
        reverse('how-to-set-up-expand-redirect')

    with pytest.raises(NoReverseMatch):
        reverse('how-to-set-up-home-invest-redirect')


def test_url_redirect_industries_to_about_uk_page_on(client, settings):
    settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON'] = True
    reload_urlconf(settings)

    response = client.get('/international/content/industries/')
    assert response.status_code == 302
    assert response.url == '/international/content/about-uk/industries/'

    response = client.get('/international/content/industries/automotive/')
    assert response.status_code == 302
    assert response.url == '/international/content/about-uk/industries/automotive'
    assert reverse('industries-home-to-about-uk-redirect')


def test_url_redirect_industries_to_about_uk_page_off(client, settings):
    settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON'] = False
    reload_urlconf(settings)

    with pytest.raises(NoReverseMatch):
        reverse('industries-home-to-about-uk-redirect')

    with pytest.raises(NoReverseMatch):
        reverse('industries-to-about-uk-redirect')


def test_url_redirect_international_contact_triage_on(client, settings):
    settings.FEATURE_FLAGS['INTERNATIONAL_TRIAGE_ON'] = True
    reload_urlconf(settings)

    assert reverse('international-contact-triage')

    with pytest.raises(NoReverseMatch):
        reverse('contact-page-international')


def test_url_redirect_international_contact_triage_off(client, settings):
    settings.FEATURE_FLAGS['INTERNATIONAL_TRIAGE_ON'] = False
    reload_urlconf(settings)

    assert reverse('contact-page-international')

    with pytest.raises(NoReverseMatch):
        reverse('international-contact-triage')


@pytest.mark.parametrize('url, redirect_url', [
    ('/international/content/how-to-setup-in-the-uk/', '/international/content/invest/how-to-setup-in-the-uk/'),
    ('/international/content/invest/how-to-setup-in-the-uk/', '/international/investment/')
])
def test_other_redirects(url, redirect_url, client):
    # This test is useful to move responsibility of older tests performed on now redirected URL
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == redirect_url
