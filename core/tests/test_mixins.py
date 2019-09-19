import pytest
import requests_mock
from unittest.mock import patch

from django.views.generic import TemplateView
from core import mixins
from core.header_config import tier_one_nav_items, tier_two_nav_items
from core.mixins import InternationalHeaderMixin
from core.tests.helpers import create_response

from directory_constants.choices import COUNTRY_CHOICES, EU_COUNTRIES


@pytest.mark.parametrize('method,expected', (
    ('get', '"c6d6f2e3e546f8bc48487537e339e7a5"'),
    ('post', None),
    ('patch', None),
    ('put', None),
    ('delete', None),
    ('head', None),
    ('options', None),
))
def test_set_etag_mixin(rf, method, expected):
    class MyView(mixins.SetEtagMixin, TemplateView):

        template_name = 'core/test_template.html'

        def post(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def patch(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def put(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def delete(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def head(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def options(self, *args, **kwargs):
            return super().get(*args, **kwargs)

    request = getattr(rf, method)('/')
    request.sso_user = None
    view = MyView.as_view()
    response = view(request)

    response.render()
    assert response.get('Etag') == expected


@pytest.mark.parametrize('view_class', mixins.SetEtagMixin.__subclasses__())
def test_cached_views_not_dynamic(rf, settings, view_class):
    # exception will be raised if the views perform http request, which are an
    # indicator that the views rely on dynamic data.
    with requests_mock.mock():
        view = view_class.as_view()
        request = rf.get('/')
        request.LANGUAGE_CODE = 'en-gb'
        # highlights if the view tries to interact with the session, which is
        # also an indicator that the view relies on dynamic data.
        request.session = None
        response = view(request)
        assert response.status_code == 200


@pytest.mark.parametrize('country_code', [code for code, _ in COUNTRY_CHOICES])
@patch('directory_components.helpers.get_user_country')
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_country_region(mock_cms_response, mock_country, country_code, rf):
    class TestView(mixins.RegionalContentMixin, TemplateView):
        template_name = 'core/base.html'

    mock_cms_response.return_value = create_response(
        json_payload={
            'title': 'test',
            'meta': {
                'languages': [('en-gb', 'English')]
            }
        }
    )

    mock_country.return_value = country_code

    request = rf.get('/', {'country': country_code})
    response = TestView.as_view()(request)

    if country_code in EU_COUNTRIES:
        assert response.context_data['region'] == 'eu'
    else:
        assert not response.context_data['region']


def test_international_header_mixin():
    class TestView(InternationalHeaderMixin, TemplateView):
        template_name = 'core/base.html'
        header_section = tier_one_nav_items.ABOUT_UK
        header_sub_section = tier_two_nav_items.INDUSTRIES

    context_data = TestView().get_context_data()

    assert context_data['header_section'] == 'about-uk'
    assert context_data['header_sub_section'] == 'industries'
