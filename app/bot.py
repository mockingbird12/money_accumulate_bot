import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.user_state import UserState

import keyboards

from db_engine import DB_driver
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
async def cmd_list(message: types.Message):
    print('Просмотр')
    await message.answer("Просмотр")
    db = DB_driver()
    total_capital = 0
    for one_saving in db.get_savings():
        print(one_saving)
        value = db.get_saving_value(one_saving.name)
        print(f'value {value}')
        total_capital += value
        await message.answer(f"{one_saving} - {value}")
    await message.answer(f"Общая сумма накоплений - {total_capital}")
    # await state.set_state(UserState.watch_capital.state)


@dp.message_handler(Text(equals=config.EDITING))
async def cmd_edit(message: types.Message, state: FSMContext):
    print('Редактирование')
    keyboard = keyboards.savings()
    print('keyboard create')
    await message.answer("Выберите какое накопление вы будете редактировать",reply_markup=keyboard)
    await state.set_state(UserState.editing.state)


@dp.message_handler(Text(equals=config.CREATING))
async def create_capital(message: types.Message, state: FSMContext):
    await message.answer("Создание. Введите название накопления", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.create_new_capital.state)


@dp.message_handler(Text(equals=config.DELETE))
async def delete_capital(message: types.Message, state: FSMContext):
    delete_keyboard = keyboards.savings()
    await message.answer("Выберите что удалить:", reply_markup=delete_keyboard)
    await state.set_state(UserState.delete.state)


@dp.message_handler()
async def delete_current_capital(message: types.Message, state: FSMContext):
    user_data = message.text.lower()
    print(user_data)
    db_client = DB_driver()
    db_client.delete_saving(user_data)
    await message.answer(f"Накопление {user_data} успешно удалено")
    await state.finish()


@dp.message_handler()
async def create_current_capital(message: types.Message, state: FSMContext):
    user_data = message.text.lower()
    print(user_data)
    db_client = DB_driver()
    db_client.create_savings(user_data)
    keyboard = keyboards.start()
    await message.answer(f"Отлично накопление <{user_data}> создано", reply_markup=keyboard)
    await state.finish()


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
    keyboard = keyboards.start()
    db_client = DB_driver()
    db_client.set_saving_value(user_data['chosen_capital'],new_value)
    await message.answer(f"Накопление {user_data['chosen_capital']} Новая сумма {new_value}", reply_markup=keyboard)
    await state.finish()


dp.register_message_handler(editing_capitals, state=UserState.editing)
dp.register_message_handler(cmd_list)
dp.register_message_handler(cmd_edit)
dp.register_message_handler(start_conversation, commands="start")
dp.register_message_handler(editing_current_capital, state=UserState.editing_current_capital)
dp.register_message_handler(create_current_capital, state=UserState.create_new_capital)
dp.register_message_handler(delete_current_capital, state=UserState.delete)


if __name__ == "__main__":
    # Запускаем бота и пропускаем все накопленые входящие
    executor.start_polling(dp, skip_updates=True)