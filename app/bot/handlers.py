import os
import random

import telebot
from telebot.types import InputMediaPhoto, MenuButtonCommands, BotCommand

from bot.keyboard import keyboard_inline
from bot.utils import (
    bisect,
    get_frame,
    help_response_html,
    default_response_html,
    congratulations_html,
    not_found_html
)
from db.database import DBConnector
from logs.app_logger import telegram_logging
from utils.texts import (
    CAPTION,
    END,
    MESSAGE_NOT_MODIFIED,
    START,
    START_COMMAND,
    START_COMMAND_DESCRIPTION,
    HELP_COMMAND,
    HELP_COMMAND_DESCRIPTION
)

db = DBConnector()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN", ''))
bot.set_my_commands(
    commands=[
        BotCommand(
            command=HELP_COMMAND,
            description=HELP_COMMAND_DESCRIPTION
        ),
        BotCommand(
            command=START_COMMAND,
            description=START_COMMAND_DESCRIPTION
        )
    ]
)
bot.set_chat_menu_button(bot.get_me().id, MenuButtonCommands(type='commands'))


class BotHandlers():

    @telegram_logging
    @bot.message_handler(commands=["help"])
    def help_command(message):
        bot.send_message(
            chat_id=message.chat.id,
            text=help_response_html(),
            parse_mode="html",
            disable_web_page_preview=True
        )

    @telegram_logging
    @bot.message_handler(commands=["start"])
    def start_command(message):
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
        if call.data == 'yes' or call.data == 'no':
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
                    if chat["mid"] not in [39555, 39556]:
                        bot.send_message(
                            chat_id=chat["chat_id"], text=not_found_html(),
                            parse_mode="html",
                        )
                    else:
                        bot.send_message(
                            chat_id=chat["chat_id"],
                            text=congratulations_html(chat["mid"]),
                            parse_mode="html",
                        )

    @telegram_logging
    @bot.message_handler(func=lambda message: True)
    def all_messages(message):
        bot.reply_to(
            message=message,
            text=default_response_html(),
            parse_mode="html",
            disable_web_page_preview=True
        )
