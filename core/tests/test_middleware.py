import pytest

from django.conf import settings
from django.http import HttpResponse
from django.utils import translation

from core import middleware


def test_locale_middleware_installed():
    expected = 'core.middleware.LocaleQuerystringMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


@pytest.mark.parametrize('query_string_object,expected_language_code', (
    ({'lang': 'fr'}, 'fr'),
    ({'lang': 'en-gb'}, 'en-gb'),
    ({'language': 'de'}, 'de'),
    ({'language': 'en-gb'}, 'en-gb'),
    ({'language': 'zh-hans', 'lang': 'zh-hans'}, 'zh-hans'),
    ({'lang': 'ja', 'language': 'ja'}, 'ja'),
    ({'language': 'es', 'lang': 'ar'}, 'es'),
    ({'lang': 'pt', 'language': 'de'}, 'de'),
))
def test_locale_middleware_sets_querystring_language(
        query_string_object,
        expected_language_code,
        rf
):
    request = rf.get('/', query_string_object)
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    assert request.LANGUAGE_CODE == expected_language_code
    assert translation.get_language() == expected_language_code


def test_locale_middleware_ignored_invalid_querystring_language(rf):
    request = rf.get('/', {'language': 'plip'})
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = settings.LANGUAGE_CODE
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_middleware_handles_missing_querystring_language(rf):
    request = rf.get('/')
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = settings.LANGUAGE_CODE
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_persist_middleware_installed():
    expected = 'core.middleware.PersistLocaleMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_locale_persist_middleware_handles_no_explicit_language(client, rf):
    request = rf.get('/')
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)

    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
    assert cookie.value == settings.LANGUAGE_CODE


def test_locale_persist_middleware_persists_explicit_language(client, rf):
    language_code = 'en-gb'
    request = rf.get('/', {'lang': language_code})
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]

    assert cookie.value == language_code