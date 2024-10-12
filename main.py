import asyncio
import datetime
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import TELEGRAM_API, WEATHER_API
import requests

logging.basicConfig(level=logging.INFO)

API_TOKEN = TELEGRAM_API
weather_api = WEATHER_API

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать! Пришли мне название города в хочешь узнать погоду")


@dp.message(lambda message: message.text)
async def weather(message: types.Message):
    city = message.text
    try:
        responce = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid='
                                f'{weather_api}')
        data = responce.json()
        if data.get("cod") != 200:
            await message.reply("Проверьте название города")
        city_name = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # продолжительность дня
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        weather_info = (f"Время в городе: {city_name}\n"
                        f"Температура: {cur_temp}°C\n"
                        f"Влажность: {humidity}%\n"
                        f"Давление: {pressure} гПа\n"
                        f"Скорость ветра: {wind} м/с\n"
                        f"Восход солнца: {sunrise_timestamp.strftime('%H:%M:%S')}\n"
                        f"Закат солнца: {sunset_timestamp.strftime('%H:%M:%S')}\n"
                        f"Длительность дня: {length_of_the_day}\n")
        await message.reply(weather_info)
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
