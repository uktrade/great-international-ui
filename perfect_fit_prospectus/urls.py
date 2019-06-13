from directory_components.decorators import skip_ga360
from django.conf.urls import url
from perfect_fit_prospectus.views import PerfectFitProspectusMainView, \
    PerfectFitProspectusReportProxyView


urlpatterns = [
    url(
        '^$',
        skip_ga360(PerfectFitProspectusMainView.as_view()),
        name='main'
    ),
    url(
        '^reports/(?P<filename>.*)$',
        skip_ga360(PerfectFitProspectusReportProxyView.as_view()),
        name='report'
    ),
]
