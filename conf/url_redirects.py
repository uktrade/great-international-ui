from django.conf.urls import url

from core.views import QuerystringRedirectView


redirects_before_tree_based_routing_lookup = [
    # These ones are inserted into the urlconf before the 'cms-page-from-path' route is tried
    # so we can redirect pages that otherwise came from tree-based routing
    url(
        r'^international/content/opportunities/$',
        QuerystringRedirectView.as_view(pattern_name='atlas-opportunities'),
    ),
]

redirects = [
    url(
        r'^international/eu-exit-news/contact/$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form'),
    ),
    url(
        r'^international/eu-exit-news/contact/success/$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form-success'),
    ),

    url(
        r'^international/brexit/contact/$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form'),
    ),
    url(
        r'^international/brexit/contact/success/$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form-success'),
    ),
]
