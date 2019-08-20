from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        '^$',
        views.HomeView.as_view(),
        name='home'
    ),
    url(
        '^search/$',
        views.CompanySearchView.as_view(),
        name='search'
    ),
    url(
        '^(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        views.ContactView.as_view(),
        name='company-contact',
    ),
    url(
        '^(?P<company_number>[a-zA-Z0-9]+)/sent/$',
        views.ContactSuccessView.as_view(),
        name='company-contact-sent',
    ),
    url(
        '^(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        views.ProfileView.as_view(),
        name='profile'
    ),
    url(
        '^(?P<company_number>[a-zA-Z0-9]+)/$',
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
