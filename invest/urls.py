from django.conf.urls import url

from directory_components.decorators import skip_ga360

from . import views

urlpatterns = [
    url(
        r"^$",
        skip_ga360(views.InvestHomePage.as_view()),
        name="index"
    ),
]
