import requests
import django

django.setup()
from forecast.models import Hourly, Daily
from apscheduler.schedulers.blocking import BlockingScheduler


API_KEY = "72d9f1b84db72c2f09b1ca979af0e3c3"
COUNTRY_CODE = "BR"


def get_open_weather_data():
    get_forecast_per_city()
    scheduler = BlockingScheduler()
    scheduler.add_job(get_forecast_per_city, "interval", hours=24)
    scheduler.start()


def get_cities_Centro_Oeste():
    # IBGE API gets all cities from Centro-Oeste
    link = f"https://servicodados.ibge.gov.br/api/v1/localidades/regioes/5/municipios"
    request = requests.get(link)
    request_json = request.json()
    cities_states = dict()
    for city in request_json:
        city_name = city["nome"]
        state_name = city["microrregiao"]["mesorregiao"]["UF"]["nome"]
        cities_states[city_name] = state_name
    return cities_states


def get_forecast_per_city():
    try:
        cities_states = get_cities_Centro_Oeste()

        for city in cities_states:
            city_name = city
            state_name = cities_states[city]

            city_weather_hourly = get_forecast_city(city_name, state_name)

            if city_weather_hourly is not None:
                city_daily_analysis(city_weather_hourly)

    except Exception as e:
        raise e


def get_forecast_city(city_name, state_name):
    link = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{COUNTRY_CODE}&appid={API_KEY}&limit{1}"
    request = requests.get(link)
    if request.ok:
        city_weather_hourly = []
        request_json = request.json()
        # request_json['list'] receives a forecast for the next 5 days in 3h intervals, each "time" is one of this intervals
        for time in request_json["list"]:
            date = time["dt_txt"]
            temp = time["main"]["temp"] - 273.15
            humidity = time["main"]["humidity"]
            try:
                rain = time["rain"]["3h"]
            except:
                rain = 0

            model_hourly = Hourly(
                city_name=city_name,
                state_name=state_name,
                date=date,
                temp=temp,
                humidity=humidity,
                rain=rain,
            )
            try:
                hourly_obj, created = Hourly.objects.update_or_create(
                    city_name=city_name,
                    date=date,
                    defaults={
                        "state_name": state_name,
                        "temp": temp,
                        "humidity": humidity,
                        "rain": rain,
                    },
                )

                if created:
                    print(city_name, date, "hourly forecast was inserted successfully")
                else:
                    print(city_name, date, "hourly forecast was updated successfully")

            except Exception as e:
                raise e

            city_weather_hourly.append(model_hourly)
        return city_weather_hourly


def city_daily_analysis(city_weather_hourly):
    days = {}
    for hour in city_weather_hourly:
        forecast_day = hour.date.split(" ")[0] + " 00:00:00"

        if forecast_day not in days:
            days[forecast_day] = {
                "hours_quantity": 1,
                "model_daily": Daily(
                    city_name=hour.city_name,
                    state_name=hour.state_name,
                    date=forecast_day,
                    temp=hour.temp,
                    temp_min=hour.temp,
                    temp_max=hour.temp,
                    humidity=hour.humidity,
                    rain=hour.rain,
                ),
            }
        else:
            model_daily = days[forecast_day]["model_daily"]

            if model_daily.temp_min > hour.temp:
                model_daily.temp_min = hour.temp

            if model_daily.temp_max < hour.temp:
                model_daily.temp_max = hour.temp

            model_daily.temp += hour.temp
            model_daily.humidity += hour.humidity
            model_daily.rain += hour.rain

            days[forecast_day]["hours_quantity"] += 1

    for day in days.values():
        if day["hours_quantity"] == 8:
            day["model_daily"].temp /= 8
            day["model_daily"].humidity /= 8

            try:
                daily_obj, created = Daily.objects.update_or_create(
                    city_name=day["model_daily"].city_name,
                    date=day["model_daily"].date,
                    defaults={
                        "state_name": day["model_daily"].state_name,
                        "temp": day["model_daily"].temp,
                        "temp_min": day["model_daily"].temp_min,
                        "temp_max": day["model_daily"].temp_max,
                        "humidity": day["model_daily"].humidity,
                        "rain": day["model_daily"].rain,
                    },
                )

                if created:
                    print(
                        day["model_daily"].city_name,
                        day["model_daily"].date,
                        "daily forecast was inserted successfully",
                    )
                else:
                    print(
                        day["model_daily"].city_name,
                        day["model_daily"].date,
                        "daily forecast was updated successfully",
                    )
            except Exception as e:
                raise e
