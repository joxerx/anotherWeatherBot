import logging

import aiogram.types
from aiogram import Bot, Dispatcher, executor, types, utils
import inline_keyboard

import config
import messages
from coordinates import Coordinates

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_API_TOKEN, parse_mode="html")
dp = Dispatcher(bot)

'''
users_coordinates = {
    userId = {'coordinates' = [], handledData = data}, 
    userId2 = {'coordinates' = [], handledData = data},
    userId3 = {'coordinates' = [], handledData = data}
}
'''
users_coordinates = {

}


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    if message.from_user.id not in users_coordinates:
        users_coordinates[message.from_user.id] = {
            'coordinates': [message.location.latitude, message.location.longitude]
        }
    else:
        if 'handledData' in users_coordinates[message.from_user.id]:
            with open('out'+ message.from_user.id+ str(users_coordinates[message.from_user.id]['coordinates']) + '.txt', "w") as file:
                file.write(str(users_coordinates[message.from_user.id]['handledData']))
            file.close()
            del users_coordinates[message.from_user.id]['handledData']
        users_coordinates[message.from_user.id]['coordinates'] = [message.location.latitude, message.location.longitude]
    reply = "Позиция обновлена!"
    await message.answer(reply,
                         reply_markup=inline_keyboard.SETLOCATION)


@dp.message_handler(commands=['setlocation'])
async def cmd_locate_me(message: types.Message):
    reply = "Нажмите кнопку ниже, чтобы отправить текущую геопозицию."
    await message.answer(reply,
                         reply_markup=inline_keyboard.SETLOCATION)


@dp.message_handler(commands=['weather'])
async def show_weather(message: types.Message):
    if not in users_coordinates[message.from_user.id]:
        users_coordinates[message.from_user.id] = {
            'coordinates': [message.location.latitude, message.location.longitude]
        }
    else:
        users_coordinates[message.from_user.id]['coordinates'] = [message.location.latitude, message.location.longitude]
    await message.answer(text=messages.weather(),
                         reply_markup=inline_keyboard.WEATHER)


@dp.message_handler(commands=['start', 'help'])
async def show_help_message(message: types.Message):
    await message.answer(
        text=f'С помощью бота можно узнать погоду в точке на карте.',
        reply_markup=inline_keyboard.HELP)


@dp.message_handler(commands='forecast')
async def show_forecast(message: types.Message):
    await message.answer(text=messages.forecast(),
                         reply_markup=inline_keyboard.FORECAST)


@dp.message_handler(commands='sun_time')
async def show_sun_time(message: types.Message):
    await message.answer(text=messages.sun_time(),
                         reply_markup=inline_keyboard.SUN_TIME)


@dp.callback_query_handler(text='weather')
async def process_callback_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.weather(),
        reply_markup=inline_keyboard.WEATHER
    )


@dp.callback_query_handler(text='wind')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.wind(),
        reply_markup=inline_keyboard.WIND
    )


@dp.callback_query_handler(text='sun_time')
async def process_callback_sun_time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.sun_time(),
        reply_markup=inline_keyboard.SUN_TIME
    )


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Отправить геопозицию", request_location=True)
    keyboard.add(button)
    return keyboard



'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
'''
