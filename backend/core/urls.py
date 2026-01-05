from django.urls import path
from .views import health

urlpatterns = [
    path("health/", health),
]

from django.urls import path
from .views import health, rates

urlpatterns = [
    path("health/", health),
    path("rates/", rates),
]
