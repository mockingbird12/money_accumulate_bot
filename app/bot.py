import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from os import getenv
from sys import exit

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="Просмотр накоплений")
async def cmd_list(message: types.Message):
    await message.reply("Просмотр")

@dp.message_handler(commands="Редактирование")
async def cmd_edit(message: types.Message):
    await message.reply("Просмотр")

dp.register_message_handler(cmd_list, commands="Просмотр накоплений")
dp.register_message_handler(cmd_edit, commands="Редактирование")

if __name__ == "__main__":
    # Запускаем бота и пропускаем все накопленые входящие
    executor.start_polling(dp, skip_updates=True)