from urllib.parse import urlencode

from django.urls import reverse


def get_paginator_url(filters):
    url = reverse('investment-support-directory:search')
    # Hack for AWS WAF 403 caused by spaces in 'on' within the querystring
    field = 'expertise_products_services_human_resources'
    if filters.get(field):
        filters[field] = [item.replace(' ', '-') for item in filters[field]]
    if filters.get('expertise_products_services_labels'):
        del filters['expertise_products_services_labels']

    querystring = urlencode({
        key: value
        for key, value in filters.items()
        if value and key != 'page'
    }, doseq=True)
    return f'{url}?{querystring}'
