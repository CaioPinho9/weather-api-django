# Weather API

This is the documentation for my Weather Api.

```
pip install -r requirements.txt
python -m flask run
```
If it doesn't run successfully, try using python3

### `GET /forecast_hourly`

Returns a list of forecast data for the next 5 days, with information in 3-hour intervals.

#### Query Parameters

- `start_date`: Start date of forecast interval. It's possible to use past dates to get historical data.
- `end_date`: (optional) End date of forecast interval. The default is the equal to start_date.
- `cities`: (optional) Specifies which city or cities you want receive forecast data.
- `states`: (optional) Specifies which state or states you want receive forecast data.

#### Body Examples

```json
{
  "start_date": "2023-02-20 00:00:00",
  "cities": "Brasília"
}
```

```json
{
  "start_date": "2023-02-20 00:00:00",
  "end_date": "2023-02-21 23:00:00",
  "cities": ["Brasília", "Goiânia"]
}
```

```json
{
  "start_date": "2023-02-20",
  "states": "Mato Grosso"
}
```

```json
{
  "start_date": "2023-02-20"
}
```

#### Response Exemple

```json
{
  "cities": [
        {
            "city_name": "Água Clara",
            "dates": [
                {
                    "date": "2023-02-20 00:00:00",
                    "humidity": 83.0,
                    "rain": 0.0,
                    "temp": 21.02
                }
            ],
            "state_name": "Mato Grosso do Sul"
        },
        {
            "city_name": "Amambai",
            "dates": [
                {
                    "date": "2023-02-20 00:00:00",
                    "humidity": 94.0,
                    "rain": 0.0,
                    "temp": 18.81
                }
            ],
            "state_name": "Mato Grosso do Sul"
        },
        {...}
  ]
}
```

- `cities`
  - `city_name`: The name of the city
  - `state_name`: The name of the state
  - `dates`: Collection of forecast dates
    - `date`: The date and time of the forecast
    - `humidity`: Humidity, %
    - `rain`: Rain volume for the last 3 hours, mm
    - `temp`: Temperature. Unit Default: Celsius.

### `GET /forecast_daily`

Returns a list of forecast data for the next 5 days, with information in daily intervals.

#### Query Parameters

- `start_date`: Start date of forecast interval. It's possible to use past dates to get historical data
- `end_date`: (optional) End date of forecast interval. The default is the equal to start_date.
- `cities`: (optional) Specifies which city or cities you want receive forecast data.
- `states`: (optional) Specifies which state or states you want receive forecast data.

#### Body Examples

```json
{
  "start_date": "2023-02-20 00:00:00",
  "cities": "Brasília"
}
```

```json
{
  "start_date": "2023-02-20 00:00:00",
  "end_date": "2023-02-21 23:00:00",
  "cities": ["Brasília", "Goiânia"]
}
```

```json
{
  "start_date": "2023-02-20",
  "states": "Mato Grosso"
}
```

```json
{
  "start_date": "2023-02-20"
}
```

#### Response Example

```json
{
  "cities": [
        {
            "city_name": "Água Clara",
            "dates": [
                {
                    "date": "2023-02-20 00:00:00",
                    "humidity": 84.8571,
                    "rain": 0.0,
                    "temp": 21.4914,
                    "temp_max": 25.38,
                    "temp_min": 17.71
                }
            ],
            "state_name": "Mato Grosso do Sul"
        },
        {
            "city_name": "Amambai",
            "dates": [
                {
                    "date": "2023-02-20 00:00:00",
                    "humidity": 92.7143,
                    "rain": 0.0,
                    "temp": 19.8714,
                    "temp_max": 21.92,
                    "temp_min": 17.72
                }
            ],
            "state_name": "Mato Grosso do Sul"
        },
        {...}
  ]
}
```

- `cities`
  - `city_name`: The name of the city
  - `state_name`: The name of the state
  - `dates`: Collection of forecast dates
    - `date`: The date and time of the forecast
    - `humidity`: Humidity, %
    - `rain`: Rain volume for the day, mm
    - `temp`: Average temperature. Unit Default: Celsius.
    - `temp_min`: Minimum temperature. Unit Default: Celsius.
    - `temp_max`: Maximum temperature. Unit Default: Celsius.
