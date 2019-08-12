from django.conf.urls import url

import core.views
from core.views import QuerystringRedirectView
from . import views


urlpatterns = [
    url(
        r'^$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': '/trade/'},
        name='trade-home'
    ),
    url(
        r'^subscribe/$',
        views.AnonymousSubscribeFormView.as_view(),
        name='trade-subscribe'
    ),
    url(
        r'^subscribe/success/$',
        views.AnonymousSubscribeSuccessView.as_view(),
        name='trade-subscribe-success'
    ),
    url(
        r'^international/content/trade/$',
        QuerystringRedirectView.as_view(pattern_name='trade-home'),
        name='content-trade-home-redirect'
    ),
]
