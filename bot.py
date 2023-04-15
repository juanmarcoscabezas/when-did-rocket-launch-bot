import os
import random
import telebot
import math

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)
from telebot.apihelper import ApiTelegramException
from dotenv import load_dotenv
from db import DB
from logger import telegram_logging

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CAPTION = 'Did the rocket launch?'
START = 0
END = 61695
bot = telebot.TeleBot(BOT_TOKEN)


def get_frame(frame=1000):
    return f'http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/{frame}/'

def build_mesage(frame_url):
    markdown = '[ENLACE]({})'.format(frame_url)
    return markdown

def keyboard_inline():
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(
        InlineKeyboardButton('Yes', callback_data='yes'),
        InlineKeyboardButton('No', callback_data='no')
    )
    return keyboard

def bisect(chat, message):
    if message == 'yes':
        chat['right'] = chat['mid']
        chat['mid'] = int(math.ceil((chat['right'] + chat['left']) / 2))
    if message == 'no':
        chat['left'] = chat['mid']
        chat['mid'] = int(math.ceil((chat['right'] + chat['left']) / 2))
    chat['attempts'] = chat['attempts'] + 1
    db.update_chat(chat_id=chat['chat_id'], data=chat)

@telegram_logging
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help command", reply_markup=keyboard_inline())

@telegram_logging
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_data = {
        'chat_id': message.chat.id,
        'left': START,
        'right': END,
        'mid': random.randint(START, END),
        'attempts': 0,
        'finished': False,
    }
    bot.send_chat_action(chat_data['chat_id'], 'upload_photo')
    db.create_chat(data=chat_data)
    bot.send_photo(
        message.chat.id,
        photo=get_frame(chat_data['mid']),
        caption=CAPTION,
        reply_markup=keyboard_inline()
    )


@bot.callback_query_handler(func=lambda msg: True)
@telegram_logging
def callback_query(call):
    chat = db.find_chat(chat_id=call.message.chat.id)
    bot.send_chat_action(chat['chat_id'], 'upload_photo')
    bisect(chat, call.data)
    try:
        bot.edit_message_media(
            chat_id=chat['chat_id'],
            message_id=call.message.id,
            media=InputMediaPhoto(get_frame(chat['mid']), caption=CAPTION),
            reply_markup=keyboard_inline(),
        )
    except ApiTelegramException as e:
        if 'message is not modified: specified new message content and reply markup are exactly the same' in str(e):
            bot.edit_message_reply_markup(chat_id=chat['chat_id'], message_id=call.message.id)
            bot.send_message(
                chat_id=chat['chat_id'],
                text='Congratulations, you have found the frame in which the rocket launches, The frame is number "{}"'.format(chat['mid'])
            )

if __name__ == '__main__':
    db = DB()
    bot.infinity_polling()
