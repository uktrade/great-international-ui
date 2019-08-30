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


def test_investment_support_directory_feature_off(settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = False
    reload_urlconf(settings)

    with pytest.raises(NoReverseMatch):
        reverse('investment-support-directory:home')


def test_investment_support_directory_feature_on(settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True
    reload_urlconf(settings)

    assert reverse('investment-support-directory:home')


def test_url_redirect_expand_page_on(client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = True
    reload_urlconf(settings)

    response = client.get('/international/invest/incoming/foo/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'

    response = client.get('/international/invest/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'

    response = client.get('/international/content/invest/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'

    response = client.get('/international/invest/contact/')
    assert response.status_code == 302
    assert response.url == '/international/expand/contact'

    response = client.get('/international/invest/contact/success/')
    assert response.status_code == 302
    assert response.url == '/international/expand/contact/success'

    response = client.get('/international/content/invest/high-potential-opportunities/')
    assert response.status_code == 302
    assert response.url == '/international/content/expand/high-potential-opportunities'

    response = client.get('/international/content/expand/high-potential-opportunities/')
    assert response.status_code == 302
    assert response.url == '/international/content/expand/#high-potential-opportunities'

    response = client.get('/international/invest/incoming/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'


def test_url_redirect_expand_page_off(client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    response = client.get('/international/invest/incoming/foo/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'

    response = client.get('/international/expand/')
    assert response.status_code == 200

    response = client.get('/international/invest/')
    assert response.status_code == 200

    response = client.get('/international/content/invest/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'

    response = client.get('/international/content/expand/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'

    response = client.get('/international/content/invest/high-potential-opportunities/')
    assert response.status_code == 302
    assert response.url == '/international/content/invest/#high-potential-opportunities'

    response = client.get('/international/invest/incoming/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'
