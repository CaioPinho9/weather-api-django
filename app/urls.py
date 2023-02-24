"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from multiprocessing import Process

from rest_framework import routers

from forecast.api import viewsets as dailyviewsets
from forecast.api import viewsets as hourlyviewsets

from forecast.api.open_weather_api import get_open_weather_data
from forecast import views

p = Process(target=get_open_weather_data)
p.start()

route = routers.DefaultRouter()

route.register(
    r"forecast_daily",
    dailyviewsets.DailyViewSet,
    basename="Daily",
)

route.register(
    r"forecast_hourly",
    hourlyviewsets.HourlyViewSet,
    basename="Hourly",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(route.urls)),
    path("", views.index),
]