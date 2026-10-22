"""Проверка обработки ошибок в функции get_data."""
from weather import get_data, ApiError, FORECAST_URL

CASES = [
    ("Неверные параметры (широта 999)", FORECAST_URL, {"latitude": 999, "longitude": 0, "current": "temperature_2m"}),
    ("Несуществующий сервер", "https://api.open-meteo.invalid/v1/forecast", None),
    ("Сервер отвечает дольше 10 секунд", "https://httpbin.org/delay/15", None),
]

for title, url, params in CASES:
    try:
        get_data(url, params)
        print(f"{title}: ошибки нет")
    except ApiError as error:
        print(f"{title}:\n  Ошибка: {error}")
