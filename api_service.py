import json
from dataclasses import dataclass
from datetime import datetime

import requests

import config
from coordinates import Coordinates


condition_dict = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом'
}
wind_dir_dict = {
    'nw': 'северо-западное',
    'n': 'северное',
    'ne': 'северо-восточное',
    'e': 'восточное',
    'se': 'юго-восточное',
    's': 'южное',
    'sw': 'юго-западное',
    'w': 'западное',
    'c': 'штиль'
}
daytime_dict = {
    'd': 'день',
    'n': 'ночь'
}
prec_type_dict = {
    0: 'без осадков',
    1: 'дождь',
    2: 'дождь со снегом',
    3: 'снег',
    4: 'град'
}
prec_strength_dict = {
    0: '',
    0.25: 'слабый ',
    0.5: '',
    0.75: 'сильный ',
    1: 'очень сильный '
}
cloudness = {
    0: 'ясно',
    0.25: 'малооблачно',
    0.5: 'облачно с прояснениями',
    0.75: 'облачно с прояснениями',
    1: 'пасмурно'
}


@dataclass(slots=True, frozen=True)
class FactWeather:
    temp: float  # cesium
    feels_like: float
    condition: str  # need to convert to words
    wind_speed: float  # m/s
    wind_gust: float
    wind_dir: str  # need to convert words
    pressure: float  # mm
    humidity: float  # need to convert to percent
    daytime: str  # need to convert day/night
    obs_time: datetime
    prec_type: int  # need to convert to str
    prec_strength: float  # need to identify and show strength
    cloudness: str  # need to convert to words


@dataclass(slots=True, frozen=True)
class Part:
    temp_min: float
    temp_max: float
    temp_avg: float
    feels_like: float
    condition: str
    wind_speed: float
    wind_gust: float
    wind_dir: str
    pressure: float
    humidity: float
    prec_mm: float  # expected mm precipitation
    prec_type: int  # need to convert to type of precipitation
    prec_strength: float  # need to convert to words type and strength
    cloudness: float  # need to convert to words


@dataclass(slots=True, frozen=True)
class Short:
    temp: float
    feels_like: float
    condition: str  # need to convert to words
    wind_speed: float
    wind_gust: float
    wind_dir: str
    pressure: float
    humidity: float
    prec_mm: float  # expected mm precipitation
    prec_type: int  # need to convert to type of precipitation
    prec_strength: float  # need to convert to words type and strength
    cloudness: float  # need to convert to words


@dataclass(slots=True, frozen=True)
class Parts:
    night: Part
    morning: Part
    day: Part
    evening: Part
    day_short: Short
    night_short: Short


@dataclass(slots=True, frozen=True)
class Forecast:
    date_ts: datetime  # unix time
    week: int
    sunrise: str
    sunset: str
    moon_code: int  # need to convert to words
    parts: Parts


@dataclass(slots=True, frozen=True)
class CityInfo:
    def_pressure: float
    url: str


@dataclass(slots=True, frozen=True)
class Answer:
    now: datetime
    info: CityInfo
    geo_object: str
    fact: FactWeather
    forecasts: Forecast


def get_city_info(ya_weather_dict: dict) -> CityInfo:
    return CityInfo(
        def_pressure=ya_weather_dict['info']['def_pressure_mm'],
        url=ya_weather_dict['info']['url']
    )


def get_fact_weather(ya_weather_dict: dict) -> FactWeather:
    return FactWeather(
        temp=ya_weather_dict['fact']['temp'],
        feels_like=ya_weather_dict['fact']['feels_like'],
        condition=condition_dict[ya_weather_dict['fact']['condition']],
        wind_speed=ya_weather_dict['fact']['wind_speed'],
        wind_gust=ya_weather_dict['fact']['wind_gust'],
        wind_dir=wind_dir_dict[ya_weather_dict['fact']['wind_dir']],
        pressure=ya_weather_dict['fact']['pressure_mm'],
        humidity=ya_weather_dict['fact']['humidity'],
        daytime=daytime_dict[ya_weather_dict['fact']['daytime']],
        obs_time=datetime.fromtimestamp(ya_weather_dict['fact']['obs_time']),
        prec_type=ya_weather_dict['fact']['humidity'],
        prec_strength=ya_weather_dict['fact']['humidity'],
        cloudness=cloudness[ya_weather_dict['fact']['cloudness']]
    )


def get_one_part(ya_weather_dict: dict) -> Part:
    return Part(
        temp_min=ya_weather_dict['temp_min'],
        temp_avg=ya_weather_dict['temp_avg'],
        temp_max=ya_weather_dict['temp_max'],
        feels_like=ya_weather_dict['feels_like'],
        condition=ya_weather_dict['condition'],
        wind_speed=ya_weather_dict['wind_speed'],
        wind_gust=ya_weather_dict['wind_gust'],
        wind_dir=ya_weather_dict['wind_dir'],
        pressure=ya_weather_dict['pressure'],
        humidity=ya_weather_dict['humidity'],
        prec_mm=ya_weather_dict['prec_mm'],
        prec_type=ya_weather_dict['prec_type'],
        prec_strength=ya_weather_dict['prec_strength'],
        cloudness=ya_weather_dict['cloudness']
    )


def get_short_part(ya_weather_dict: dict) -> Short:
    return Short(
        temp=ya_weather_dict['temp'],
        feels_like=ya_weather_dict['feels_like'],
        condition=ya_weather_dict['condition'],
        wind_speed=ya_weather_dict['wind_speed'],
        wind_gust=ya_weather_dict['wind_gust'],
        wind_dir=ya_weather_dict['wind_dir'],
        pressure=ya_weather_dict['pressure'],
        humidity=ya_weather_dict['humidity'],
        prec_mm=ya_weather_dict['prec_mm'],
        prec_type=ya_weather_dict['prec_type'],
        prec_strength=ya_weather_dict['prec_strength'],
        cloudness=ya_weather_dict['cloudness']
    )


def get_parts_forecast(ya_weather_dict: dict) -> Parts:
    return Parts(
        night=get_one_part(ya_weather_dict['night']),
        morning=get_one_part(ya_weather_dict['morning']),
        day=get_one_part(ya_weather_dict['day']),
        evening=get_one_part(ya_weather_dict['evening']),
        day_short=get_short_part(ya_weather_dict['day_short']),
        night_short=get_short_part(ya_weather_dict['night_short'])
    )


def get_forecasts(ya_weather_dict: dict) -> Forecast:
    return Forecast(
        date_ts=datetime.fromtimestamp(ya_weather_dict['forecasts'][0]['date_ts']),
        week=ya_weather_dict['forecasts'][0]['week'],
        sunrise=ya_weather_dict['forecasts'][0]['sunrise'],
        sunset=ya_weather_dict['forecasts'][0]['sunset'],
        moon_code=ya_weather_dict['forecasts'][0]['moon_code'],
        parts=get_parts_forecast(ya_weather_dict['forecasts'][0]['parts'])
    )


def parse_string_answer(ya_weather_response: str) -> Answer:
    ya_weather_dict = json.loads(ya_weather_response)
    return Answer(
        now=datetime.fromtimestamp(ya_weather_dict['now']),
        info=get_city_info(ya_weather_dict),
        geo_object=ya_weather_dict['geo_object']['district']['name'],
        fact=get_fact_weather(ya_weather_dict),
        forecasts=get_forecasts(ya_weather_dict)
    )


def get_full_answer(coordinates=Coordinates) -> Answer:
    """"Generates Answer as object to manipulate with"""
    yandex_response = get_yandex_weather_response(
        longitude=coordinates.longitude,
        latitude=coordinates.latitude
    )
    full_answer = parse_string_answer(yandex_response)
    return full_answer


def get_yandex_weather_response(latitude: float, longitude: float) -> str:
    url = config.HEADER_YANDEX_API_CALL.format(latitude=latitude, longitude=longitude)
    return requests.get(url, headers=config.HEADER_YANDEX_API_CALL).text
