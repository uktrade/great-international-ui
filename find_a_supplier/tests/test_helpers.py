from django.urls import reverse

from find_a_supplier import helpers


def test_get_paginator_url():
    filters = {'page': 2, 'term': 'foo', 'industries': None}

    assert helpers.get_paginator_url(filters) == (
        reverse('find-a-supplier:search') + '?term=foo'
    )


def test_get_paginator_url_multiple_filters():
    filters = {
        'industries': ['AEROSPACE', 'AGRICULTURE_HORTICULTURE_AND_FISHERIES'],
    }

    encoded_url = (
        '?industries=AEROSPACE'
        '&industries=AGRICULTURE_HORTICULTURE_AND_FISHERIES'
    )

    assert helpers.get_paginator_url(filters) == (
            reverse('find-a-supplier:search') + encoded_url
    )
