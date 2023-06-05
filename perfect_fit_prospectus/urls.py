from django.urls import re_path
from perfect_fit_prospectus.views import PerfectFitProspectusMainView, \
    PerfectFitProspectusReportProxyView, PerfectFitProspectusSuccessView


app_name = 'perfect_fit_prospectus'

urlpatterns = [
    re_path(
        '^$',
        PerfectFitProspectusMainView.as_view(),
        name='main'
    ),
    re_path(
        '^success/$',
        PerfectFitProspectusSuccessView.as_view(),
        name='success'
    ),
    re_path(
        '^reports/(?P<filename>.*)$',
        PerfectFitProspectusReportProxyView.as_view(),
        name='report'
    ),
]
