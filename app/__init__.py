from flask import Flask
from telebot import TeleBot

from app.helpers.firebase import initFirebase

from json import loads

with open("config/config.json", "r") as configFile:
    data = configFile.read()

config = loads(data)

API_TOKEN = config["token"]
CHANNELS = config["channels"]

app = Flask(__name__)
bot = TeleBot(API_TOKEN)

initFirebase()

from app import routes