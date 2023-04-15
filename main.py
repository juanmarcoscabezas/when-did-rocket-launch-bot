import time
import os


from dotenv import load_dotenv
from flask import Flask, request

from waitress import serve  # type: ignore

from bot.handlers import bot, telebot
from utils.ngrok import ngrok_config

load_dotenv()

flask_server = Flask(__name__)


@flask_server.route("/", methods=["GET"])
def index():
    return "OK", 200


@flask_server.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200


if __name__ == "__main__":
    SERVER_PORT = os.getenv("SERVER_PORT")
    ENV = os.getenv("ENV")
    BOT_POLLING = os.getenv("BOT_POLLING")
    PROD_SERVER_URL = os.getenv("PROD_SERVER_URL")

    bot.remove_webhook()
    time.sleep(1)

    if BOT_POLLING == "True":
        bot.infinity_polling()
    else:
        if ENV == "prod":
            bot.set_webhook(url=PROD_SERVER_URL)
            serve(flask_server, host="0.0.0.0", port=SERVER_PORT)
        else:
            ngrok_url = ngrok_config()
            bot.set_webhook(url=ngrok_url)
            flask_server.run(host="0.0.0.0", port=SERVER_PORT)
