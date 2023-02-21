from rest_framework import serializers
from forecast import models


class DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Daily
        fields = "__all__"


class HourlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hourly
        fields = "__all__"
