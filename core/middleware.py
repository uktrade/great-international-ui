from django.utils.deprecation import MiddlewareMixin
import re


class GoogleCampaignMiddleware(MiddlewareMixin):
    """This middleware captures the various utm*
    querystring parameters and saves them in session."""

    UTM_CODES = ['utm_source',
                 'utm_medium',
                 'utm_campaign',
                 'utm_term',
                 'utm_content']

    def process_request(self, request):
        if not request.session.get('utm'):
            request.session['utm'] = {}

        if request.GET.get('utm_source'):
            utm = {}

            for code in self.UTM_CODES:
                value = request.GET.get(code)
                if value:
                    utm[code] = value

            request.session['utm'] = utm

        # store utm codes on the request object,
        # so they're available in templates
        request.utm = request.session['utm']


class MicrosoftDefenderSafeLinksMiddleware(MiddlewareMixin):
    """PII in the form of email addresses is injected into links by a
    MS 365 email client as values to a 'data' parameter.
    
    These 'safe links' don't appear to have a consistent pattern, the small sample
    data available looks like:

    - /international/content/opportunities/<https://eur02..safelinks.protection.outlook.com/ \
        ?url=[url]&data=[PII!]&sdata=[sdata]&reserved=0

    - /international/trade/<https://eur02.safelinks.protection.outlook.com/ \
        ?url=[url]&data=[PII!]&sdata=[sdata]&reserved=0

    - /international/?amp;data=[PII!]&amp;sdata=[sdata]&amp;reserved=0&lang=en-gb

    - /international/?lang=zh-hans<https://eur02.safelinks.protection.outlook.com/ \
        ?url=[url]?lang=zh-hans&data=[PII!]&sdata=[sdata]&reserved=0

    - /international/invest/<https://eur02.safelinks.protection.outlook.com/ \
        ?url=[url]&data=[PII!]&sdata=[sdata]&reserved=0>.

    This middleware removes the 'data' parameter and its value from a request path
    that is added by Microsoft 365 Defender, thus PII does not get captured in Google Analytics."""

    SAFE_LINKS_REGEX = r'[&|amp;]data=.*?\|[\w\.-]+@[\w\.-]+(?:\.[\w]+)+\|.*?(?=&)'

    def process_request(self, request):
        clean_query_string = re.sub(self.SAFE_LINKS_REGEX, '', request.META['QUERY_STRING'])

        request.META['QUERY_STRING'] = clean_query_string
