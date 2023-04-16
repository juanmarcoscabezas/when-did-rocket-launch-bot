from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def keyboard_inline():
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(
        InlineKeyboardButton('Yes', callback_data='yes'),
        InlineKeyboardButton('No', callback_data='no')
    )
    return keyboard
