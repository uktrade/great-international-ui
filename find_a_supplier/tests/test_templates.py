import pytest
from bs4 import BeautifulSoup
from django.utils import translation
from django.template.loader import render_to_string


@pytest.mark.parametrize('lang,exp_industries', [
    ('en-gb', 3),
    ('de', 2),
    ('ja', 1),
])
def test_fas_homepage_industry_list(lang, exp_industries, fas_home_page):
    page = {
        'industries': [
            {
                'title': 'Aerospace',
                'meta': {
                    'languages': [
                        ['en-gb', 'English'],
                        ['de', 'Deutsch'],
                    ],
                }
            },
            {
                'title': 'Agricultural technology',
                'meta': {
                    'languages': [
                        ['en-gb', 'English'],
                        ['de', 'Deutsch'],
                    ],
                }
            },
            {
                'title': 'Automotive',
                'meta': {
                    'languages': [
                        ['en-gb', 'English'],
                        ['ja', '日本語'],
                    ],
                }
            },
        ],
        **fas_home_page
    }
    context = {
        'page': page
    }
    with translation.override(lang):
        print(lang)
        html = render_to_string('find_a_supplier/landing_page.html', context)
        soup = BeautifulSoup(html, 'html.parser')
        industries = soup.find(id='industries-section').findAll('li')
        assert len(industries) == exp_industries
