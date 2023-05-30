from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

main_menu = ['Просмотр накоплений', 'Редактирование накоплений']

class UserState(StatesGroup):
    start = State()
    delete = State()
    waiting_decision = State()
    watch_capital = State()
    select_assert_currency = State()
    editing = State()
    editing_current_capital = State()
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
        await state.set_state(UserState.watch_capital.state)
    if message.text.lower() == 'Редактирование накоплений':
        print('Редактирование накоплений')
        await state.set_state(UserState.editing.state)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(user_start, commands="start", state="*")
    dp.register_message_handler(decision_make, state=UserState.waiting_decision)
    dp.register_message_handler()
