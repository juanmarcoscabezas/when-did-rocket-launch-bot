import os
import random

import telebot
from telebot.types import InputMediaPhoto

from bot.keyboard import keyboard_inline
from bot.utils import bisect, get_frame
from db.database import DBConnector
from logs.app_logger import telegram_logging
from utils.texts import (
    CAPTION,
    CONGRATULATIONS,
    END,
    MESSAGE_NOT_MODIFIED,
    START
)

db = DBConnector()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN", ''))


class BotHandlers():

    @telegram_logging
    @bot.message_handler(commands=["help"])
    def send_welcome(message):
        bot.reply_to(message, "Help command", reply_markup=keyboard_inline())

    @telegram_logging
    @bot.message_handler(commands=["start"])
    def message_handler(message):
        chat_data = {
            "chat_id": message.chat.id,
            "left": START,
            "right": END,
            "mid": random.randint(START, END),
            "attempts": 0,
            "finished": False,
        }
        bot.send_chat_action(chat_data["chat_id"], "upload_photo")
        db.create_chat(data=chat_data)
        bot.send_photo(
            message.chat.id,
            photo=get_frame(chat_data["mid"]),
            caption=CAPTION,
            reply_markup=keyboard_inline(),
        )

    @bot.callback_query_handler(func=lambda msg: True)
    @telegram_logging
    def callback_query(call):
        chat = db.find_chat(chat_id=call.message.chat.id)
        bot.send_chat_action(
            chat_id=chat["chat_id"], action="upload_photo", timeout=1)
        updated_chat = bisect(chat, call.data)
        try:
            if chat["right"] - chat["left"] < 1:
                raise Exception(MESSAGE_NOT_MODIFIED)
            else:
                bot.edit_message_media(
                    chat_id=chat["chat_id"],
                    message_id=call.message.id,
                    media=InputMediaPhoto(
                        get_frame(chat["mid"]), caption=CAPTION),
                    reply_markup=keyboard_inline(),
                )
                db.update_chat(
                    chat_id=updated_chat["chat_id"], data=updated_chat)
        except Exception as e:
            if MESSAGE_NOT_MODIFIED in str(e):
                bot.edit_message_reply_markup(
                    chat_id=chat["chat_id"], message_id=call.message.id
                )
                bot.send_message(
                    chat_id=chat["chat_id"], text=CONGRATULATIONS.format(
                        chat["mid"])
                )