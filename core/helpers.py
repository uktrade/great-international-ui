from django.utils import translation
import requests


def create_response(status_code=200, json_payload=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_payload or {}
    return response


def unslugify(slug):
    return slug.replace('-', ' ').capitalize()


def get_language_from_querystring(request):
    language_codes = translation.trans_real.get_languages()
    language_code = request.GET.get('lang')
    if language_code and language_code in language_codes:
        return language_code
