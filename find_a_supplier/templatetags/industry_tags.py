from collections import OrderedDict
import itertools
import urllib.parse

from directory_constants.sectors import CONFLATED

from django import template
from django.urls import reverse


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
