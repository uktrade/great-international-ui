from directory_components.decorators import skip_ga360
from django.conf.urls import url
from perfect_fit_prospectus.views import PerfectFitProspectusMainView, \
    PerfectFitProspectusReportProxyView, PerfectFitProspectusSuccessView


urlpatterns = [
    url(
        '^$',
        skip_ga360(PerfectFitProspectusMainView.as_view()),
        name='main'
    ),
    url(
        '^success/$',
        skip_ga360(PerfectFitProspectusSuccessView.as_view()),
        name='success'
    ),
    url(
        '^reports/(?P<filename>.*)$',
        skip_ga360(PerfectFitProspectusReportProxyView.as_view()),
        name='report'
    ),
]
