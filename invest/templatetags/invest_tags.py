import re

from bs4 import BeautifulSoup

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def get_first_heading(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(re.compile(r'h\d+'))[0].string
