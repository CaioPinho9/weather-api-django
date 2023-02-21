from django.db import models

# Create your models here.


class Daily(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, null=False)
    city_name = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    date = models.DateTimeField()
    temp = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    humidity = models.FloatField()
    rain = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["city_name", "date"], name="city_date_daily")
        ]


class Hourly(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, null=False)
    city_name = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    date = models.DateTimeField()
    temp = models.FloatField()
    humidity = models.FloatField()
    rain = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["city_name", "date"], name="city_date_hourly")
        ]
