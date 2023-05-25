from django.urls import re_path

from . import views

app_name = 'investment-support-directory'

urlpatterns = [
    re_path(
        '^$',
        views.HomeView.as_view(),
        name='home'
    ),
    re_path(
        '^search/$',
        views.CompanySearchView.as_view(),
        name='search'
    ),
    re_path(
        '^(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        views.ContactView.as_view(),
        name='company-contact',
    ),
    re_path(
        '^(?P<company_number>[a-zA-Z0-9]+)/sent/$',
        views.ContactSuccessView.as_view(),
        name='company-contact-sent',
    ),
    re_path(
        '^(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        views.ProfileView.as_view(),
        name='profile'
    ),
    re_path(
        '^(?P<company_number>[a-zA-Z0-9]+)/$',
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
]
