from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from forecast.api import serializers
from forecast import models

from forecast.api.view_utils import view_utils


class DailyViewSet(viewsets.ModelViewSet):
    def list(self, request):
        params = view_utils.format_params(request)

        queryset = view_utils.select_filter(params, models.Daily)

        json = view_utils.json(
            serializers.DailySerializer(queryset, many=True), "daily"
        )
        return json

class HourlyViewSet(viewsets.ModelViewSet):
    def list(self, request):
        params = view_utils.format_params(request)

        queryset = view_utils.select_filter(params, models.Hourly)

        json = view_utils.json(
            serializers.HourlySerializer(queryset, many=True), "hourly"
        )
        return json
