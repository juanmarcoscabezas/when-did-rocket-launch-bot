from pyngrok import conf, ngrok
import os
from dotenv import load_dotenv

load_dotenv()
NGROK_TOKEN = os.getenv("NGROK_TOKEN")
SERVER_PORT = os.getenv("SERVER_PORT")


def ngrok_config():
    conf.get_default().config_path = "./config_ngrok.yml"
    conf.get_default().region = "eu"
    ngrok.set_auth_token(NGROK_TOKEN)

    ngrok_tunel = ngrok.connect(SERVER_PORT, bind_tls=True)
    ngrok_url = ngrok_tunel.public_url
    print("URL NGROK:", ngrok_url)
    return ngrok_url
