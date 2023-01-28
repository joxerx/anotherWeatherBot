from api_service import Answer


def weather(answer: Answer) -> str:
    """Returns a message about the temperature and weather description"""
    return f'В {answer.geo_object} за окном сейчас: {answer.fact.condition}, по ощущениям {answer.fact.feels_like}°C\n'\
           f'Скорость ветра {answer.fact.wind_speed}м/с,с порывами до {answer.fact.wind_gust}м/с.'


def forecast(answer: Answer) -> str:
    """Returns a message about wind direction and speed"""
    return f'Минимальная температура на {answer.forecasts.date_ts}: {answer.forecasts.parts.day.temp_min}°C.\n' \
           f'Максимальная:  {answer.forecasts.parts.day.temp_min}°C.\n' \
           f'Средняя:  {answer.forecasts.parts.day.temp_avg}°C.\n'

'''
coordinates = Coordinates(latitude=59.916515, longitude=30.351841)
print(weather(get_full_answer(Coordinates)))

'''

