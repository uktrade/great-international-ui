import re
import dateparser

from bs4 import BeautifulSoup

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.text import slugify
from django.utils import translation


register = template.Library()


def build_anchor_id(element):
    return slugify(get_label(element) + '-section')


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element)
    return str(soup)


@register.filter
def table_of_contents(value):
    soup = BeautifulSoup(value, 'html.parser')
    return [
        (build_anchor_id(element), get_label(element))
        for element in soup.findAll('h2')
    ]


@register.filter
def first_paragraph(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('p')
    return str(element)


@register.filter
def first_image(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('img')
    if not element:
        return ''
    del element['height']
    return element


@register.filter
def grouper(value, n):
    ungrouped = value or []
    return [ungrouped[x:x+n] for x in range(0, len(ungrouped), n)]


@register.filter
def add_export_elements_classes(value):
    soup = BeautifulSoup(value, 'html.parser')
    mapping = [
        ('h2', 'heading-large'),
        ('h3', 'heading-medium'),
        ('ul', 'list list-bullet'),
        ('ol', 'list list-number'),
        ('a', 'link'),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs['class'] = class_name
    return str(soup)


@register.filter
def convert_headings_to(value, heading):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        element.name = heading
    return str(soup)


@register.filter
def override_elements_css_class(value, element_and_override):
    arguments = element_and_override.split(',')
    element_type = arguments[0]
    override = arguments[1]
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll(element_type):
        element.attrs['class'] = override
    return str(soup)


@register.filter
def add_href_target(value, request):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('a', attrs={'href': re.compile("^http")}):
        if request.META['HTTP_HOST'] not in element.attrs['href']:
            element.attrs['target'] = '_blank'
    return str(soup)


@register.filter
def filter_by_active_language(pages):
    return [page for page in pages if is_translated_to_current_language(page)]


def is_translated_to_current_language(page):
    active_language = translation.get_language()
    for code, _ in page['meta']['languages']:
        if code == active_language:
            return True
    else:
        return False


@register.filter(is_safe=True)
@stringfilter
def title_from_heading(heading):
    if ':' in heading:
        return heading.split(':')[0].strip()
    # full width character used in ja and zh
    if '：' in heading:
        return heading.split('：')[0].strip()
    return heading


@register.filter
def parse_date(date_string):
    if date_string:
        return dateparser.parse(date_string).strftime('%d %B %Y')
    return None


@register.filter
def prefix_path(path):
    return '/international' + path


@register.filter
def add_with_arrow_to_link(value):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('a'):
        element.attrs['class'] = 'link with-arrow'
    return str(soup)
