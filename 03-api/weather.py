"""
Скрипт получения прогноза погоды через открытый API Open-Meteo.

Пользователь вводит название города, скрипт:
1) находит координаты города (Geocoding API),
2) получает текущую погоду и прогноз на несколько дней (Forecast API),
3) выводит результат в виде таблиц.
Запросы можно повторять в цикле, пока пользователь не введёт «выход».
"""

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10  # секунд ожидания ответа от сервера

# Коды погоды WMO -> понятное описание
WEATHER_CODES = {
    0: "Ясно", 1: "Преимущественно ясно", 2: "Переменная облачность", 3: "Пасмурно",
    45: "Туман", 48: "Изморозь",
    51: "Слабая морось", 53: "Морось", 55: "Сильная морось",
    61: "Слабый дождь", 63: "Дождь", 65: "Сильный дождь",
    71: "Слабый снег", 73: "Снег", 75: "Сильный снег",
    80: "Ливень", 81: "Ливень", 82: "Сильный ливень",
    95: "Гроза", 96: "Гроза с градом", 99: "Гроза с градом",
}


class ApiError(Exception):
    """Ошибка при обращении к API."""


def get_data(api_url, params=None):
    """Отправляет GET-запрос к API и возвращает ответ в виде словаря (JSON)."""
    try:
        response = requests.get(api_url, params=params or {}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # ошибка, если код ответа 4xx или 5xx
        return response.json()
    except requests.exceptions.Timeout as error:
        raise ApiError("Сервер не ответил вовремя") from error
    except requests.exceptions.ConnectionError as error:
        raise ApiError("Нет соединения с сервером") from error
    except requests.exceptions.HTTPError as error:
        # Open-Meteo в теле ответа объясняет, что не так с запросом
        try:
            reason = response.json().get("reason", "")
        except ValueError:
            reason = ""
        raise ApiError(f"Неверный запрос (HTTP {response.status_code}) {reason}".strip()) from error
    except ValueError as error:
        raise ApiError("Сервер вернул ответ не в формате JSON") from error


def find_city(name):
    """Ищет город по названию и возвращает его данные (координаты, страна)."""
    data = get_data(GEOCODING_URL, {"name": name, "count": 1, "language": "ru"})
    results = data.get("results")
    if not results:
        raise ApiError(f"Город «{name}» не найден")
    return results[0]


def get_weather(latitude, longitude, days):
    """Получает текущую погоду и прогноз на указанное число дней."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
                   "wind_speed_10m,weather_code",
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum,weather_code",
        "wind_speed_unit": "ms",
        "timezone": "auto",
        "forecast_days": days,
    }
    return get_data(FORECAST_URL, params)


def print_table(headers, rows):
    """Печатает таблицу: ширина каждого столбца подбирается по самому длинному значению."""
    widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
    line = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(row):
        return "| " + " | ".join(str(item).ljust(width) for item, width in zip(row, widths)) + " |"

    print(line)
    print(format_row(headers))
    print(line.replace("-", "="))
    for row in rows:
        print(format_row(row))
    print(line)


def show_weather(city, weather):
    """Выводит текущую погоду и прогноз по дням в виде таблиц."""
    current = weather["current"]
    units = weather["current_units"]

    print(f"\nПогода: {city['name']}, {city.get('country', '')} "
          f"({city['latitude']:.2f}, {city['longitude']:.2f})")
    print("\nСейчас:")
    print_table(
        ["Параметр", "Значение"],
        [
            ["Время", current["time"].replace("T", " ")],
            ["Температура", f"{current['temperature_2m']} {units['temperature_2m']}"],
            ["Ощущается как", f"{current['apparent_temperature']} {units['apparent_temperature']}"],
            ["Влажность", f"{current['relative_humidity_2m']} {units['relative_humidity_2m']}"],
            ["Ветер", f"{current['wind_speed_10m']} м/с"],
            ["Описание", WEATHER_CODES.get(current["weather_code"], "Неизвестно")],
        ],
    )

    daily = weather["daily"]
    rows = []
    for i, date in enumerate(daily["time"]):
        rows.append([
            date,
            f"{daily['temperature_2m_min'][i]:+.1f}",
            f"{daily['temperature_2m_max'][i]:+.1f}",
            f"{daily['precipitation_sum'][i]:.1f}",
            WEATHER_CODES.get(daily["weather_code"][i], "Неизвестно"),
        ])
    print(f"\nПрогноз на {len(rows)} дн.:")
    print_table(["Дата", "Мин, °C", "Макс, °C", "Осадки, мм", "Погода"], rows)


def ask_days():
    """Спрашивает число дней прогноза (1–16). По умолчанию — 3."""
    answer = input("На сколько дней прогноз (1-16, Enter = 3): ").strip()
    if not answer:
        return 3
    if not answer.isdigit() or not 1 <= int(answer) <= 16:
        print("Нужно число от 1 до 16, беру 3 дня.")
        return 3
    return int(answer)


def main():
    """Основной цикл: запрашиваем город, пока пользователь не введёт «выход»."""
    print("Прогноз погоды (Open-Meteo API). Для выхода введите «выход».")
    while True:
        name = input("\nГород: ").strip()
        if name.lower() in ("выход", "exit", "q"):
            print("До свидания!")
            break
        if not name:
            print("Введите название города.")
            continue

        days = ask_days()
        try:
            city = find_city(name)
            weather = get_weather(city["latitude"], city["longitude"], days)
            show_weather(city, weather)
        except ApiError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
