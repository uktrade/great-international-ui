import pytest
from bs4 import BeautifulSoup


from django.template import Context, Template

def test_banner():
    banner_content = {
        'badge_content': 'Badge content',
        'banner_content': '<p>Banner content with a <a href="#">link</a></p>',
    }
    string = (
        "{{% load banner from industry_tags %}}"
        "{{% banner badge_content='{badge_content}' "
        "banner_content='{banner_content}' %}}"
        ).format(**banner_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    banner = soup.select('.great-information-banner')[0]
    assert banner['id'] == 'information-banner'

    badge = soup.select('.banner-badge span')[0]
    assert badge.string == 'Badge content'

    exp_banner_content = (
        '<div><p class="govuk-body">Banner content with a '
        '<a class="link" href="#">link</a></p></div>')

    banner_content = soup.select('.banner-content div:nth-of-type(2)')[0]
    assert str(banner_content) == exp_banner_content


@pytest.mark.parametrize('input_html,expected_html', (
    ('<h1>content</h1>', '<h1 class="govuk-heading-xl great-text-white">content</h1>'),
    ('<h2>content</h2>', '<h2 class="govuk-heading-l">content</h2>'),
    ('<h3>content</h3>', '<h3 class="govuk-heading-m">content</h3>'),
    ('<h4>content</h4>', '<h4 class="govuk-heading-s">content</h4>'),
    ('<ul>content</ul>', '<ul class="list list-bullet">content</ul>'),
    ('<ol>content</ul>', '<ol class="list list-number">content</ol>'),
    ('<p>content</p>', '<p class="govuk-body">content</p>'),
    ('<a>content</a>', '<a class="govuk-link">content</a>'),
    ('<blockquote>a</blockquote>', '<blockquote class="quote">a</blockquote>')
))
def test_add_export_elements_classes(input_html, expected_html):
    template = Template(
        '{% load add_export_elements_classes from industry_tags %}'
        '{{ html|add_export_elements_classes }}'

    )
    context = Context({'html': input_html})

    html = template.render(context)
    assert html == expected_html