import time
import os


from dotenv import load_dotenv
from flask import Flask, request

from waitress import serve  # type: ignore

from bot.handlers import bot, telebot
from utils.ngrok import ngrok_config

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "OK", 200


@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200


if __name__ == "app":
    SERVER_PORT = os.getenv("SERVER_PORT")
    ENV = os.getenv("ENV")
    BOT_POLLING = os.getenv("BOT_POLLING")

    bot.remove_webhook()
    time.sleep(1)

    if BOT_POLLING == "True":
        bot.infinity_polling()
    else:
        ngrok_url = ngrok_config()
        if ENV == "prod":
            print("Production server")
            bot.set_webhook(url=ngrok_url)
            serve(app, host="0.0.0.0", port=SERVER_PORT)
        else:
            bot.set_webhook(url=ngrok_url)
            app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
