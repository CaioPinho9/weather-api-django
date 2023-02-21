from rest_framework import viewsets
from forecast.api import serializers
from forecast import models


class DailyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DailySerializer
    queryset = models.Daily.objects.all()


class HourlyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HourlySerializer
    queryset = models.Hourly.objects.all()
