from bs4 import BeautifulSoup
from collections import OrderedDict
import itertools
import urllib.parse

from directory_constants.sectors import CONFLATED

from django import template
from django.urls import reverse
from django.utils.html import mark_safe


register = template.Library()


@register.simple_tag
def search_url(sector_value=None, term=None):
    if isinstance(sector_value, str):
        sector_value = [sector_value]

    params = OrderedDict()

    if sector_value:
        industries = [CONFLATED.get(item, {item}) for item in sector_value]
        params['industries'] = list(itertools.chain(*industries))
    if term:
        params['term'] = term
    querystring = urllib.parse.urlencode(params, doseq=True)
    return reverse('find-a-supplier:search') + '?' + querystring


@register.filter
def add_export_elements_classes(value, color):
    soup = BeautifulSoup(value, 'html.parser')
    mapping = [
        ('h1', 'govuk-heading-xl great-text-white'),
        ('h2', 'govuk-heading-l'),
        ('h3', 'govuk-heading-m'),
        ('h4', 'govuk-heading-s'),
        ('h5', 'govuk-heading-s'),
        ('h6', 'govuk-heading-s'),
        ('ul', 'list list-bullet'),
        ('ol', 'list list-number'),
        ('p', 'govuk-body-white' if color == 'W' else 'govuk-body'),
        ('a', 'link'),
        ('blockquote', 'quote'),
        ('strong', 'great-bold-small'),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs['class'] = class_name
    return mark_safe(str(soup))


@register.filter
def convert_headings_to(value, heading):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        element.name = heading
    return str(soup)


@register.inclusion_tag('find_a_supplier/banner.html')
def banner(**kwargs):
    return kwargs
