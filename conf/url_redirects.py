from django.conf.urls import url

from core.views import QuerystringRedirectView

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
