from flask import Flask, request
from bot.handlers import bot, telebot
from pyngrok import ngrok, conf
from dotenv import load_dotenv
from waitress import serve
import os
import time

load_dotenv()

flask_server = Flask(__name__)


@flask_server.route('/', methods=['GET'])
def index():
    return 'OK', 200


@flask_server.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types\
            .Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200


if __name__ == '__main__':
    SERVER_PORT = os.getenv('SERVER_PORT')
    NGROK_TOKEN = os.getenv('NGROK_TOKEN')
    ENV = os.getenv('ENV')
    BOT_POLLING = os.getenv('BOT_POLLING')

    bot.remove_webhook()
    time.sleep(1)

    if BOT_POLLING == 'True':
        bot.infinity_polling()

    conf.get_default().config_path = './config_ngrok.yml'
    conf.get_default().region = 'eu'
    ngrok.set_auth_token(NGROK_TOKEN)

    ngrok_tunel = ngrok.connect(SERVER_PORT, bind_tls=True)
    ngrok_url = ngrok_tunel.public_url
    print('URL NGROK:', ngrok_url)

    bot.set_webhook(url=ngrok_url)
    if ENV == 'prod':
        serve(flask_server, host='0.0.0.0', port=SERVER_PORT)
    else:
        flask_server.run(host='0.0.0.0', port=SERVER_PORT)
