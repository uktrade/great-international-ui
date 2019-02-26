from django.conf import settings

from core import helpers


class CountryMiddleware:
    def process_request(self, request):
        country_code = helpers.get_country_from_querystring(request)
        if country_code:
            request.COUNTRY_CODE = country_code

    def process_response(self, request, response):
        """
        Shares config with the language cookie as they serve a similar purpose
        """

        if hasattr(request, 'COUNTRY_CODE'):
            response.set_cookie(
                key=settings.COUNTRY_COOKIE_NAME,
                value=request.COUNTRY_CODE,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN
            )
        return response
