from urllib.parse import urlencode

from django.core.urlresolvers import reverse


def get_paginator_url(filters):
    url = reverse('find-a-supplier:search')
    querystring = urlencode({
        key: value
        for key, value in filters.items()
        if value and key != 'page'
    }, doseq=True)
    return f'{url}?{querystring}'
