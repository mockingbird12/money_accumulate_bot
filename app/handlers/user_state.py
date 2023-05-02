from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

main_menu = ['Просмотр накоплений', 'Редактирование накоплений']

class UserState(StatesGroup):
    waiting_decision = State()
    watch_capital = State()
    editing = State()
    editing_exsistent_capital = State()
    create_new_capital = State()

async def user_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in main_menu:
        keyboard.add(name)
    await message.answer("Выберите действие:", reply_markup=keyboard)
    await state.set_state(UserState.waiting_decision.state)


async def decision_make(message: types.Message, state: FSMContext):
    if message.text.lower() not in main_menu:
        await message.answer("Пожалуйста, выберите действие, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_decision=message.text.lower())
    if message.text.lower() == 'Просмотр накоплений':
        print('Просмотр накоплений')
    if message.text.lower() == 'Редактирование накоплений':
        print('Редактирование накоплений')
