from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_WEATHER = InlineKeyboardButton('Погода сейчас', callback_data='weather')
BTN_FORECAST = InlineKeyboardButton('Прогноз', callback_data='forecast')
BTN_SETLOCATION = InlineKeyboardButton('Обновить локацию', callback_data='setlocation')


WEATHER = InlineKeyboardMarkup().add(BTN_FORECAST, BTN_SETLOCATION)
FORECAST = InlineKeyboardMarkup().add(BTN_WEATHER).add(BTN_SETLOCATION)
SETLOCATION = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_FORECAST)
HELP = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_FORECAST).add(BTN_SETLOCATION)
