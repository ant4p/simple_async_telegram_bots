import os

import asyncio
import requests

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer('Привет! Введи:  /random_dog')

@dp.message(Command('random_dog'))
async def random_dog_handler(message: Message):
    contents = requests.get('https://random.dog/woof.json', timeout=None).json()
    url = contents['url']
    await message.answer_photo(photo=url)


async def main() -> None:
    bot = Bot(token=TOKEN_BOT)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
