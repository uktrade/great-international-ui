import re

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def update_query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query.__setitem__(key, value)
    return query.urlencode()


@register.inclusion_tag('investment_atlas/includes/collapsible_text.html')
def collapse_text(html, text_id):
    parts = re.split("<hr/?>", html, 1)
    return {
        'id': text_id,
        'initial': parts[0],
        'collapsed': parts[1] if len(parts) > 1 else None
    }


@register.simple_tag()
def cms_url():
    return settings.DIRECTORY_CMS_API_CLIENT_BASE_URL
