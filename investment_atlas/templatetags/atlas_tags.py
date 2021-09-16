from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def update_query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query.__setitem__(key, value)
    return query.urlencode()
