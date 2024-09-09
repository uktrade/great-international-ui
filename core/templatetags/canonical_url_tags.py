from django import template
from django.utils.safestring import mark_safe

from core.utils import (
    derive_absolute_url,
    derive_canonical_url,
    hreflang_and_x_default_link,
)


register = template.Library()

PATH_POS = 1
PATH_STR = '/international/investment-support-directory/'


@register.simple_tag(takes_context=True)
def get_canonical_url(context):
    request = context['request']
    if request.path.startswith(PATH_STR):
        request.path = request.path.partition(PATH_STR)[PATH_POS]
    return derive_canonical_url(request)


@register.simple_tag(takes_context=True)
def get_hreflang_tags(context):
    canonical_url = get_canonical_url(context)
    request = context['request']
    absolute_url = derive_absolute_url(request)
    if absolute_url == canonical_url:
        return mark_safe(hreflang_and_x_default_link(canonical_url))
    return mark_safe('')
