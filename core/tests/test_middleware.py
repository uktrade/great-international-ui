import pytest

from django.conf import settings
from django.http import HttpResponse

from directory_constants.constants.choices import COUNTRY_CHOICES

from core import middleware


def test_country_middleware_installed():
    expected = 'core.middleware.CountryMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_country_middleware_no_country_code(client, rf):
    request = rf.get('/')
    response = HttpResponse()
    request.session = client.session
    instance = middleware.CountryMiddleware()

    instance.process_request(request)
    instance.process_response(request, response)

    assert not hasattr(response.cookies, settings.COUNTRY_COOKIE_NAME)


@pytest.mark.parametrize('country_code,country_name', COUNTRY_CHOICES)
def test_country_middleware_sets_country_cookie(
    client, rf, country_code, country_name
):
    request = rf.get('/', {'country': country_code})
    response = HttpResponse()
    request.session = client.session
    instance = middleware.CountryMiddleware()

    instance.process_request(request)
    instance.process_response(request, response)
    cookie = response.cookies[settings.COUNTRY_COOKIE_NAME]

    assert cookie.value == country_code
