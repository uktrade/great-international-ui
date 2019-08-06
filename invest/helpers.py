LANGUAGE_CODES = ('es', 'de', 'fr', 'pt', 'zh-hans', 'ar', 'ja')


def slash_split(string):
    if string.count('/') == 1:
        return string.split('/')[0]
    else:
        return ''.join(string.split('/', 2)[:2])


def get_language_from_prefix(path):
    prefix = slash_split(path)
    if prefix in LANGUAGE_CODES:
        return prefix
