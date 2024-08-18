import translate
import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN_FROM_ENV')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


with open('mincraft_blocks.json', 'r', encoding='utf-8') as file:
    images = json.load(file)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer('Привіт! Напиши мені назву блока, і я відправлю картинку крафту або напиши команду "/crafts" i я вiдправлю тобi всi крафти.')


@dp.message(Command(commands=['crafts']))
async def send_craft_list(message: types.Message) -> None:
    keys = list(images.keys())
    num_messenges = 2
    keys_per_message = len(keys) // num_messenges + (len(keys) % num_messenges > 0)
    parts = [keys[i:i+keys_per_message] for i in range(0, len(keys), keys_per_message)]
    for part in parts:
        craft_items = ', '.join(part)
        await message.answer(f'Список доступних предметів для крафту:\n{craft_items}')


@dp.message()
async def send_message(message: types.Message) -> None:
    query = message.text
    if query in images:
        await message.answer_photo(images[query], caption=query)
    else:
        await message.answer('Немає такого предмету. Перевiрь чи правильно ти написав блок, але якщо перевiривши його дiйсно немає то напиши розробнику "https://t.me/IvanLubenskiy"')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
