from django import template

from core.utils import derive_canonical_url

register = template.Library()

PATH_POS = 1
PATH_STR = '/international/investment-support-directory/'


@register.simple_tag(takes_context=True)
def get_canonical_url(context):
    breakpoint()
    request = context['request']
    if request.path.startswith(PATH_STR):
        request.path = request.path.partition(PATH_STR)[PATH_POS]
    return derive_canonical_url(request)
