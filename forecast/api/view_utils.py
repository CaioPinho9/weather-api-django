import datetime
from django.http import JsonResponse


class view_utils:
    def format_params(request):
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        cities = request.data.get("cities")
        states = request.data.get("states")

        if start_date is None:
            start_date = datetime.date.today()

        if end_date is None:
            end_date = start_date

        if isinstance(cities, str):
            cities = [cities]
        elif cities is not None:
            cities = cities

        if isinstance(states, str):
            states = [states]
        elif states is not None:
            states = states

        return {
            "start_date": start_date,
            "end_date": end_date,
            "cities": cities,
            "states": states,
        }

    def select_filter(params, model):
        start_date = params["start_date"]
        end_date = params["end_date"]
        cities = params["cities"]
        states = params["states"]

        queryset = None

        if cities is not None:
            for city_name in cities:
                if queryset is None:
                    queryset = model.objects.filter(
                        date__gte=start_date,
                        date__lte=end_date,
                        city_name=city_name,
                    )
                else:
                    queryset = queryset | model.objects.filter(
                        date__gte=start_date,
                        date__lte=end_date,
                        city_name=city_name,
                    )
        if states is not None:
            for state in states:
                if queryset is None:
                    queryset = model.objects.filter(
                        date__gte=start_date,
                        date__lte=end_date,
                        state_name=state,
                    )
                else:
                    queryset = queryset | model.objects.filter(
                        date__gte=start_date,
                        date__lte=end_date,
                        state_name=state,
                    )

        if cities is None and states is None:
            queryset = model.objects.filter(
                date__gte=start_date,
                date__lte=end_date,
            )

        return queryset

    def json(list_model_weather, responseType):
        weather_dict = {"cities": []}
        for data in list_model_weather.data:
            city_name = data["city_name"]
            state_name = data["state_name"]
            date = datetime.datetime.strptime(
                data["date"], "%Y-%m-%dT%H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S")
            temp = data["temp"]
            humidity = data["humidity"]
            rain = data["rain"]

            if responseType == "daily":
                temp_min = data["temp_min"]
                temp_max = data["temp_max"]

            if not any(
                city["city_name"] == city_name for city in weather_dict["cities"]
            ):
                cities = weather_dict["cities"]
                cities.append(
                    {
                        "city_name": city_name,
                        "state_name": state_name,
                        "dates": [],
                    }
                )
                weather_dict["cities"] = cities

            if date not in weather_dict["cities"][-1]["dates"]:
                dates = weather_dict["cities"][-1]["dates"]
                dates.append(
                    {
                        "date": date,
                        "temp": temp,
                        "humidity": humidity,
                        "rain": rain,
                    }
                )

                if responseType == "daily":
                    dates[-1].update(
                        {
                            "temp_min": temp_min,
                            "temp_max": temp_max,
                        }
                    )

                weather_dict["cities"][-1]["dates"] = dates

        return JsonResponse(weather_dict)
