import re

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def update_query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        if value:
            query.__setitem__(key, value)
        else:
            query.pop(key, None)

    return f'?{query.urlencode()}' if query else ''


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


@register.inclusion_tag('investment_atlas/includes/chosen_filters.html', takes_context=True)
def chosen_filters(context, filter_name, applied_filters):
    filters = []

    for filter in applied_filters:
        remove_url = context['request'].path
        query = context['request'].GET.copy()
        query_filter = query.getlist(filter_name)

        if query_filter:
            query_filter.remove(filter)
            query.setlist(filter_name, query_filter)
            updated_query = query.urlencode()

            if updated_query:
                remove_url += '?' + updated_query

        filters.append({
            'label': filter,
            'remove_url': remove_url
        })
    return {
        'chosen_filters': filters
    }
