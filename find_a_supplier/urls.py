from django.urls import re_path

import core.views

from . import views

app_name = 'find-a-supplier'

urlpatterns = [
    re_path(
        r'^$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'trade'},
        name='trade-home'
    ),
    re_path(
        r'^subscribe/$',
        views.SubscribeFormView.as_view(),
        name='subscribe'
    ),
    re_path(
        r'^contact/$',
        views.IndustryLandingPageContactCMSView.as_view(),
        {'path': 'trade/contact'},
        name='industry-contact'
    ),
    re_path(
        r'^contact/success/$',
        views.IndustryLandingPageContactCMSSuccessView.as_view(),
        {'path': 'trade/contact'},
        name='industry-contact-success'
    ),
    re_path(
        r'^subscribe/success/$',
        views.AnonymousSubscribeSuccessView.as_view(),
        name='subscribe-success'
    ),
    re_path(
        r'^search/$',
        views.CompanySearchView.as_view(),
        name='search',
    ),
    re_path(
        r'^suppliers/$',
        views.PublishedProfileListView.as_view(),
        name='public-company-profiles-list',
    ),
    re_path(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        views.ContactCompanyView.as_view(),
        name='company-contact',
    ),
    re_path(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/success/$',
        views.ContactCompanySentView.as_view(),
        name='company-contact-sent',
    ),
    re_path(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        views.ProfileView.as_view(),
        name='profile',
    ),
    re_path(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/$',
        views.ProfileView.as_view(),
        name='profile-slugless'
    ),
    re_path(
        r'^case-study/(?P<id>.+)/(?P<slug>.+)/$',
        views.CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
    re_path(
        r'^case-study/(?P<id>.+)/$',
        views.CaseStudyDetailView.as_view(),
        name='case-study-details-slugless'
    ),

    re_path(
        r'^unsubscribe/$',
        views.UnsubscribeView.as_view(),
        name='unsubscribe'
    ),

]
