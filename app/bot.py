import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.user_state import UserState

import keyboards
from service_lib import get_all_savings
import config
from os import getenv
from sys import exit

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)



@dp.message_handler(commands=["start"])
async def start_conversation(message: types.Message):
    keyboard = keyboards.start()
    await message.answer('Выберите', reply_markup=keyboard)


@dp.message_handler(Text(equals=config.WATCH))
async def cmd_list(message: types.Message, state: FSMContext):
    print('Просмотр')
    await message.answer("Просмотр")
    for one_saving in get_all_savings():
        await message.answer(one_saving)
    # await state.set_state(UserState.watch_capital.state)


@dp.message_handler(Text(equals=config.EDITING))
async def cmd_edit(message: types.Message, state: FSMContext):
    print('Редактирование')
    keyboard = keyboards.savings()
    await message.answer("Редактирование",reply_markup=keyboard)
    await state.set_state(UserState.editing.state)


@dp.message_handler()
async def editing_capitals(message: types.Message, state: FSMContext):
    await message.answer(f"Введите новую сумму {message.text}", reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(chosen_capital=message.text.lower())
    await state.set_state(UserState.editing_current_capital.state)


@dp.message_handler()
async def editing_current_capital(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали:")
    user_data = await state.get_data()
    new_value = message.text
    await message.answer(f"Накопление {user_data['chosen_capital']} Новая сумма {new_value}")


dp.register_message_handler(editing_capitals, state=UserState.editing)
dp.register_message_handler(cmd_list)
dp.register_message_handler(cmd_edit)
dp.register_message_handler(start_conversation, commands="start")
dp.register_message_handler(editing_current_capital, state=UserState.editing_current_capital)


if __name__ == "__main__":
    # Запускаем бота и пропускаем все накопленые входящие
    executor.start_polling(dp, skip_updates=True)