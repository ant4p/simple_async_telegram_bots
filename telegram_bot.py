import math
import os

import asyncio
import datetime
import requests

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')
KEY_WEATHER = os.getenv('KEY_WEATHER')
bot = Bot(token=TOKEN_BOT)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет. Чтобы узнать погоду - напишите название города.")


@dp.message()
async def get_weather(message: Message) -> None:
    try:
        # await message.send_copy(chat_id=message.chat.id)
        city = message.text
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={KEY_WEATHER}",
            timeout=None
        )
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        length_day = sunset_timestamp - sunrise_timestamp

        sunrise = datetime.datetime.strftime(sunrise_timestamp, "%H:%M:%S")
        sunset = datetime.datetime.strftime(sunset_timestamp, "%H:%M:%S")

        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026a1",
            "Snow": "Снег \U0001f328",
            "Mist": "Туман \U0001f32b",
        }
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Непонятная погода..."

        await message.reply(
            f"В городе {city} \n"
            f"------------------\n"
            f"Температура: {cur_temp}°C {wd}\n"
            f"Ощущается как: {feels_like}°C\n"
            f"------------------\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {math.ceil(pressure/1.333)} мм.рт.ст\n"
            f"Ветер: {wind} м/c\n"
            f"Восход солнца: {sunrise}\n"
            f"Закат солнца: {sunset}\n"
            f"Продолжительность дня: {length_day}\n"
        )
    except Exception:
        city = message.text
        await message.reply(f"Проверьте правильность написания: {city}.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
