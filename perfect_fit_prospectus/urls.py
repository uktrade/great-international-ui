from django.conf.urls import url
from perfect_fit_prospectus.views import PerfectFitProspectusMainView, \
    PerfectFitProspectusReportProxyView, PerfectFitProspectusSuccessView


app_name = 'perfect_fit_prospectus'

urlpatterns = [
    url(
        '^$',
        PerfectFitProspectusMainView.as_view(),
        name='main'
    ),
    url(
        '^success/$',
        PerfectFitProspectusSuccessView.as_view(),
        name='success'
    ),
    url(
        '^reports/(?P<filename>.*)$',
        PerfectFitProspectusReportProxyView.as_view(),
        name='report'
    ),
]
