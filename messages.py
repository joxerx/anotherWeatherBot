from api_service import Answer


def weather(answer: Answer) -> str:
    """Returns a message about the temperature and weather description"""
    return f'По данным сервиса Яндекс Погода: \n' \
           f'{answer.geo_object}.\n' \
           f'За окном сейчас: {answer.fact.condition}.\n' \
           f'Температура воздуха: {answer.fact.temp}°C.\n' \
           f'По ощущениям {answer.fact.feels_like}°C\n' \
           f'Скорость ветра {answer.fact.wind_speed}м/с,\n' \
           f'с порывами до {answer.fact.wind_gust}м/с.'


def forecast(answer: Answer) -> str:
    """"""
    return f'Минимальная температура на {answer.forecasts.date_ts.date()}: {answer.forecasts.parts.day.temp_min}°C.\n' \
           f'Максимальная:  {answer.forecasts.parts.day.temp_max}°C.\n' \
           f'Средняя:  {answer.forecasts.parts.day.temp_avg}°C.\n' \
           f'Восход в: {answer.forecasts.sunrise}\n' \
           f'Закат: {answer.forecasts.sunset}'
