from django.conf import settings

from invest.helpers import LANGUAGE_CODES
from invest.redirects import TRANSLATED_REDIRECTS


def generate_translated_redirects_tests_params():
    tests_params = []
    for source, destination in TRANSLATED_REDIRECTS.items():
        tests_params.append((source, destination))  # add English version
        for lang_code in LANGUAGE_CODES:
            if lang_code in settings.INVEST_REDIRECTS_UNUSED_LANGUAGES:
                tests_params.append((f'{lang_code}/{source}', f'{destination}'))
            else:
                tests_params.append((f'{lang_code}/{source}', f'{destination}?lang={lang_code}'))
    return tests_params
