from flask import Flask
from json import loads

from app.helpers.firebase import initFirebase

app = Flask(__name__)

with open("config/config.json", "r") as configFile:
    data = configFile.read()

config = loads(data)

API_TOKEN = config["apiToken"]

initFirebase()

from app import routes