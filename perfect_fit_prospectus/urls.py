from django.conf.urls import url
from perfect_fit_prospectus.views import PerfectFitProspectusMainView, \
    PerfectFitProspectusReportProxyView


urlpatterns = [
    url(
        '^$',
        PerfectFitProspectusMainView.as_view(),
        name='main'
    ),
    url(
        '^reports/(?P<filename>.*)$',
        PerfectFitProspectusReportProxyView.as_view(),
        name='reports'
    ),
]
