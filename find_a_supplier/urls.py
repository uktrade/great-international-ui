from django.conf.urls import url

import core.views

from . import views


urlpatterns = [
    url(
        r'^$',
        core.views.MultilingualCMSPageFromPathView.as_view(),
        {'path': 'trade'},
        name='trade-home'
    ),
    url(
        r'^subscribe/$',
        views.SubscribeFormView.as_view(),
        name='subscribe'
    ),
    url(
        r'^contact/$',
        views.IndustryLandingPageContactCMSView.as_view(),
        {'path': 'trade/contact'},
        name='industry-contact'
    ),
    url(
        r'^contact/success/$',
        views.IndustryLandingPageContactCMSSuccessView.as_view(),
        {'path': 'trade/contact'},
        name='industry-contact-success'
    ),
    url(
        r'^subscribe/success/$',
        views.AnonymousSubscribeSuccessView.as_view(),
        name='subscribe-success'
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
        views.CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
    url(
        r'^case-study/(?P<id>.+)/$',
        views.CaseStudyDetailView.as_view(),
        name='case-study-details-slugless'
    ),
]
