import os
import urllib.parse

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from logs.logger import db_logging

load_dotenv()


class DB:
    DATABASE_NAME = urllib.parse.quote_plus(os.getenv('DATABASE_NAME'))
    DATABASE_USER = urllib.parse.quote_plus(os.getenv('DATABASE_USER'))
    DATABASE_PASSWORD = urllib.parse.quote_plus(os.getenv('DATABASE_PASSWORD'))
    database = None

    def __init__(self):
        uri = 'mongodb+srv://{}:{}@{}.kgulykm.mongodb.net/?{}'\
            .format(
                self.DATABASE_USER,
                self.DATABASE_PASSWORD,
                self.DATABASE_NAME,
                'retryWrites=true&w=majority'
            )
        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            self.database = client['test-database']
            print("Successfully connected to MongoDB")
        except Exception as e:
            print(e)

    @db_logging
    def find_chat(self, chat_id):
        return self.database.chats.find_one({'chat_id': chat_id})

    @db_logging
    def create_chat(self, data):
        found = self.find_chat(chat_id=data['chat_id'])
        if found:
            return self.update_chat(chat_id=data['chat_id'], data=data)
        return self.database.chats.insert_one(data)

    @db_logging
    def update_chat(self, chat_id, data):
        new_values = {"$set": data}
        return self.database.chats.update_one({'chat_id': chat_id}, new_values)
