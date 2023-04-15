import os
import urllib.parse

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from logs.app_logger import db_logging

load_dotenv()


class DBConnector:
    __DATABASE_NAME = urllib.parse.quote_plus(os.getenv('DATABASE_NAME', ''))
    __DATABASE_USER = urllib.parse.quote_plus(os.getenv('DATABASE_USER', ''))
    __DATABASE_PASSWORD = urllib.parse.quote_plus(
        os.getenv('DATABASE_PASSWORD', ''))
    __database = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        uri = 'mongodb+srv://{}:{}@{}.kgulykm.mongodb.net/?{}'\
            .format(
                self.__DATABASE_USER,
                self.__DATABASE_PASSWORD,
                self.__DATABASE_NAME,
                'retryWrites=true&w=majority'
            )
        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            self.__database = client['test-database']
            print("Successfully connected to MongoDB")
        except Exception as e:
            print(e)

    @db_logging
    def find_chat(self, chat_id):
        return self.__database.chats.find_one({'chat_id': chat_id})

    @db_logging
    def create_chat(self, data):
        found = self.find_chat(chat_id=data['chat_id'])
        if found:
            return self.update_chat(chat_id=data['chat_id'], data=data)
        return self.__database.chats.insert_one(data)

    @db_logging
    def update_chat(self, chat_id, data):
        new_values = {"$set": data}
        return self.__database.chats.update_one(
            {'chat_id': chat_id},
            new_values
        )
