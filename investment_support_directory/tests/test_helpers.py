from django.urls import reverse

from investment_support_directory import helpers


def test_get_paginator_url():
    filters = {'page': 2, 'term': 'foo', 'expertise_countries': None}

    assert helpers.get_paginator_url(filters) == (
        reverse('investment-support-directory:search') + '?term=foo'
    )


def test_get_paginator_url_multiple_filters():
    filters = {
        'expertise_products_services': ['EPS1_1', 'EPS1 1'],
        'expertise_languages': 'english',
        'expertise_countries': ['GB', 'fr'],
    }

    encoded_url = (
        '?expertise_products_services=EPS1_1'
        '&expertise_products_services=EPS1+1&expertise_languages'
        '=english&expertise_countries=GB&expertise_countries=fr'
    )

    assert helpers.get_paginator_url(filters) == (
            reverse('investment-support-directory:search') + encoded_url
    )


def test_get_paginator_url_403_friendly():
    filters = {
        'expertise_products_services_human_resources': [
            'Staff Onboarding', 'Space Specialist'
        ],
        'expertise_products_services_labels': [
            'I want to disappear', 'special space'
        ],
        'expertise_languages': 'english',
        'expertise_countries': ['GB', 'fr'],
    }
    encoded_url = (
        '?expertise_products_services_human_resources=Staff-Onboarding&'
        'expertise_products_services_human_resources=Space-Specialist&'
        'expertise_languages=english&expertise_countries=GB&'
        'expertise_countries=fr'
    )

    assert helpers.get_paginator_url(filters) == (
            reverse('investment-support-directory:search') + encoded_url
    )
