from aiogram import types
import config
from db_engine import DB_driver

def start():
    kb = [
        [
            types.KeyboardButton(text=config.WATCH),
            types.KeyboardButton(text=config.EDITING),
            types.KeyboardButton(text=config.CREATING),
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
    db = DB_driver()
    for i in db.get_savings():
        buttons.append(types.KeyboardButton(text=i.name))
    kb.append(buttons)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите что делать"
    )
    return keyboard