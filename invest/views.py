from django.conf import settings

from invest import helpers, redirects
from core.views import LegacyRedirectCoreView


class LegacyInvestURLRedirectView(LegacyRedirectCoreView):
    redirects_mapping = redirects.REDIRECTS
    fallback_url = '/international/investment/'

    @staticmethod
    def translate_language_from_path_to_querystring(path, params):
        if path.startswith(helpers.LANGUAGE_CODES):
            lang = helpers.get_language_from_prefix(path)
            path = path[len(lang) + 1:]  # +1 is for the /
            if lang not in settings.INVEST_REDIRECTS_UNUSED_LANGUAGES:  # these go to English
                params['lang'] = lang
        return path, params
