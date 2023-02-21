from forecast.models import Daily
from forecast.api.serializers import DailySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DailyList(APIView):
    """
    List all forecast, or create a new forecast.
    """
    def get(self, request, format=None):
        forecast = Daily.objects.all()
        serializer = DailySerializer(forecast, many=True)
        return Response(serializer.data)
      
    def get(self, request, pk, format=None):
        forecast = self.get_object(pk)
        serializer = DailySerializer(forecast)
        return Response(serializer.data)
      
  
class HourlyList(APIView):
  """
  List all forecast, or create a new forecast.
  """
  def get(self, request, format=None):
      forecast = Daily.objects.all()
      serializer = DailySerializer(forecast, many=True)
      return Response(serializer.data)
    
  def get(self, request, pk, format=None):
      forecast = self.get_object(pk)
      serializer = DailySerializer(forecast)
      return Response(serializer.data)