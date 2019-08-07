LANGUAGE_CODES = ('es', 'de', 'fr', 'pt', 'zh-hans', 'ar', 'ja')


def get_language_from_prefix(path):
    prefix = path.split('/')[0]
    if prefix in LANGUAGE_CODES:
        return prefix
