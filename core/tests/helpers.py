import requests

from unittest.mock import patch

from core.views import cms_api_client


dummy_page = {
    'title': 'test',
    'display_title': 'Title',
    'breadcrumbs_label': 'Title',
    'meta': {
        'languages': [
            ['en-gb', 'English'],
            ['fr', 'Français'],
            ['de', 'Deutsch'],
        ]
    },
    'page_type': 'InternationalHomePage',
}


def create_response(status_code=200, json_payload={}, content=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_payload
    response._content = content
    return response


def stub_page(page):
    value = create_response(json_payload={**dummy_page, **page})
    stub = patch.object(cms_api_client, 'lookup_by_path', return_value=value)
    yield stub.start()
    stub.stop()


def stub_page(page):
    value = create_response(json_payload={**dummy_page, **page})
    stub = patch.object(cms_api_client, 'lookup_by_slug', return_value=value)
    yield stub.start()
    stub.stop()
