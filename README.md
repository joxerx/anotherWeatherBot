# Очередной бот с погодой
###### Используемые технологии:
- Aiogram
- Telegram Bot API
- Yandex Weather API
- Python 3.11

###### О проекте:
За основу взял [другой проект](https://habr.com/ru/post/684038/). Захотел его доработать: узнавать погоду не по IP адресу, а по геометке. Решил использовать Yandex Weather API, поскольку возможно одним запросом получить много данных как по прогнозам, так и по текущей погоде. 
Если возникнет желание повторить, то стоит обратить внимание, что у Яндекса есть бесплатный тариф, на 50 запросов в стуки и пробный на месяц до 5000 запросов. 

###### Как работает?
Получаю ответ от сервиса Яндекс Погода, переформатирую в словарь, который затем записываю в объекты для удобного взаимодействия. 
При смене локации пользователя сохраняется информация о его последнем запросе и выполняется новый запрос.

На данный момент можно отправить любую точку на карте и запросить текущую погоду, а также короткий прогноз на день.
- /weather
- /forecast

###### В планах: 
- добавить поддержку других сервисов с погодой, чтобы можно было выбрать поставщика данных;
- добавить отправку уведомлений ко времени перед планируемым выходом;
- сделать более симпатичный и детализированный вывод

###### Установка:
- установить Aiogram
- скачать и распаковать репозиторий
- в корне проекта создать файл `config.py`
- добавить в него:
``` 
BOT_API_TOKEN = 'bot:token'`

# ВНИМАНИЕ Ниже вызов с тестовым тарифом. При использовании тарифа "Погода на вашем сайте" заменить forecast на informers:
WEATHER_YANDEX_API_CALL = ('https://api.weather.yandex.ru/v2/forecast?'
    'lat={latitude}'
    '&lon={longitude}'
    '&lang=ru_RU')
  
WEATHER_YANDEX_API_KEY = 'apiKey'
HEADER_YANDEX_API_CALL = {'X-Yandex-API-Key': WEATHER_YANDEX_API_KEY}
```
![image](https://user-images.githubusercontent.com/29130600/216273135-969f84de-19af-410c-a524-1ca09d3dfd73.png)
