from django.conf.urls import url, include

import conf.urls


urlpatterns = [
    url(
        r'^trade/',
        include(conf.urls.urlpatterns)
    )
]
