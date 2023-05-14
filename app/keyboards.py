from aiogram import types
import config
import service_lib

def start():
    kb = [
        [
            types.KeyboardButton(text=config.WATCH),
            types.KeyboardButton(text=config.EDITING),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите что делать"
    )
    return keyboard

def savings():
    kb = []
    buttons = []
    for i in service_lib.get_all_savings():
        buttons.append(types.KeyboardButton(text=i))
    kb.append(buttons)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите что делать"
    )
    return keyboard