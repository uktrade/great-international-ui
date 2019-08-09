from django.conf.urls import url

import core.views
from . import views


urlpatterns = [
    url(
        r'^$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': '/trade/'},
        name='trade-home'
    ),
    url(
        r'^search/$',
        views.CompanySearchView.as_view(),
        name='search',
    ),
    url(
        r'^suppliers/$',
        views.PublishedProfileListView.as_view(),
        name='public-company-profiles-list',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        views.ContactCompanyView.as_view(),
        name='company-contact',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/success/$',
        views.ContactCompanySentView.as_view(),
        name='company-contact-sent',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        views.ProfileView.as_view(),
        name='profile',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/$',
        views.ProfileView.as_view(),
        name='profile-slugless'
    ),
    url(
        r'^case-study/(?P<id>.+)/(?P<slug>.+)/$',
        views.CaseStudyView.as_view(),
        name='case-study-details'
    ),
    url(
        r'^case-study/(?P<id>.+)/$',
        views.CaseStudyView.as_view(),
        name='case-study-details-slugless'
    ),
]
