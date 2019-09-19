import pytest
from django.template import Context, Template
from django.urls import reverse
from django.utils import translation
from bs4 import BeautifulSoup

from core.templatetags import cms_tags

from find_a_supplier.templatetags import industry_tags


def test_search_url():
    search_url = industry_tags.search_url(
        sector_value='AEROSPACE',
        term='test',
    )

    assert search_url == (
        reverse('find-a-supplier:search') +
        '?industries=AEROSPACE&term=test'
    )


def test_convert_links_to_with_arrow():
    template = Template(
        '{% load add_export_elements_classes '
        'override_elements_css_class from directory_components %}'
        '{{ html|add_export_elements_classes|'
        'override_elements_css_class:\'a, link with-arrow\'|safe }}'

    )
    context = Context({
        'html': (
            '<a>Capital Investment</a>'
        )
    })
    html = template.render(context)

    assert html == (
        '<a class=" link with-arrow">Capital Investment</a>'
    )


def test_add_anchors():
    template = Template(
        '{% load add_anchors from cms_tags %}'
        '{{ html|add_anchors|safe }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one-section">Title one</h2>'
        '<h2 id="title-two-section">Title two</h2>'
        '<br/>'
    )


def test_table_of_contents():
    template = Template(
        '{% load table_of_contents from cms_tags %}'
        '{% for anchor, label in html|table_of_contents %}'
        '    <a href="#{{ anchor }}">{{ label }}</a>'
        '{% endfor %}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '    <a href="#title-one-section">Title one</a>'
        '    <a href="#title-two-section">Title two</a>'
    )


def test_first_paragraph():
    template = Template(
        '{% load first_paragraph from cms_tags %}'
        '{{ html|first_paragraph|safe }}'

    )
    context = Context({
        'html': '<p>The first paragraph</p><p></p>'
    })
    html = template.render(context)

    assert html == '<p>The first paragraph</p>'


def test_first_image():
    template = Template(
        '{% load first_image from cms_tags %}'
        '{{ html|first_image|safe }}'

    )
    context = Context({
        'html': (
            '<p>The first paragraph</p>'
            '<p><img src="path/to/image" height="100" width="50"/></p>'
        )
    })
    html = template.render(context)

    assert html == '<img src="path/to/image" width="50"/>'


def test_first_image_empty():
    template = Template(
        '{% load first_image from cms_tags %}'
        '{{ html|first_image|safe }}'

    )
    context = Context({
        'html': (
            '<p>The first paragraph</p>'
            '<p></p>'
        )
    })
    html = template.render(context)

    assert html == ''


def test_grouper():
    template = Template(
        '{% load grouper from cms_tags %}'
        '{% for chunk in the_list|grouper:3 %}'
        '<ul>'
        '    {% for item in chunk %}'
        '    <li>{{ item }}</li>'
        '    {% endfor %}'
        '</ul>'
        '{% endfor %}'

    )
    context = Context({
        'the_list': range(1, 10)
    })
    html = template.render(context)

    assert html == (
        '<ul>'
        '        <li>1</li>'
        '        <li>2</li>'
        '        <li>3</li>'
        '    </ul>'
        '<ul>'
        '        <li>4</li>'
        '        <li>5</li>'
        '        <li>6</li>'
        '    </ul>'
        '<ul>'
        '        <li>7</li>'
        '        <li>8</li>'
        '        <li>9</li>'
        '    </ul>'
    )


def test_grouper_remainder():
    template = Template(
        '{% load grouper from cms_tags %}'
        '{% for chunk in the_list|grouper:3 %}'
        '<ul>'
        '    {% for item in chunk %}'
        '    <li>{{ item }}</li>'
        '    {% endfor %}'
        '</ul>'
        '{% endfor %}'

    )
    context = Context({
        'the_list': range(1, 6)
    })
    html = template.render(context)

    assert html == (
        '<ul>'
        '        <li>1</li>'
        '        <li>2</li>'
        '        <li>3</li>'
        '    </ul>'
        '<ul>'
        '        <li>4</li>'
        '        <li>5</li>'
        '    </ul>'
    )


def test_add_href_target(rf):
    request = rf.get('/', HTTP_HOST='www.example.com')
    template = Template(
        '{% load add_href_target from cms_tags %}'
        '{{ html|add_href_target:request|safe }}'

    )
    context = Context({
        'request': request,
        'html': (
            '<a href="http://www.google.com"></a>'
            '<a href="https://www.google.com"></a>'
            '<a href="http://www.example.com"></a>'
            '<a href="https://www.example.com"></a>'
        )
    })
    html = template.render(context)

    assert html == (
        '<a href="http://www.google.com" target="_blank"></a>'
        '<a href="https://www.google.com" target="_blank"></a>'
        '<a href="http://www.example.com"></a>'
        '<a href="https://www.example.com"></a>'
    )


def test_filter_by_active_language(rf):
    request = rf.get('/', HTTP_HOST='www.example.com')
    translation.activate('fr')
    template = Template(
        '{% load filter_by_active_language from cms_tags %}'
        '{% for sector in sectors|filter_by_active_language %}'
        '<h1>{{ sector.title }}</h1>'
        '{% endfor %}'
    )

    test_sectors = [
        {
            'title': 'Aerospace',
            'meta': {
                'slug': 'invest-aerospace',
                'languages': [
                    ['en-gb', 'English'],
                ],
            },
        },
        {
            'title': 'Automotive',
            'meta': {
                'slug': 'invest-automotive',
                'languages': [
                    ['en-gb', 'English'],
                    ['fr', 'Français'],
                ],
            },
        },
    ]

    context = Context({
        'request': request,
        'sectors': test_sectors
    })

    filtered = template.render(context)
    soup = BeautifulSoup(filtered, 'html.parser')

    assert len(soup.find_all('h1')) == 1
    assert soup.find('h1').string == 'Automotive'


@pytest.mark.parametrize('value, expected_result', [
    ('title: heading', 'title'),
    ('アグリテック：貴社のビジネスを英国で発展させよう', 'アグリテック'),
    ('title', 'title')
])
def test_title_from_heading(value, expected_result):
    assert cms_tags.title_from_heading(value) == expected_result


def test_get_image_url_handles_missing_images():
    missing_image_result = cms_tags.get_image_url({'page': {}}, 'small_image')
    assert missing_image_result is None


def test_get_image_url_handles_image_being_none():
    none_image_result = cms_tags.get_image_url({'page': {'small_image': None}}, 'small_image')
    assert none_image_result is None
