from app import bot

from app.helpers.name import fetchName
from app.helpers.verified import isVerified
from app.helpers.retrive import retrive

from telebot import types

from firebase_admin import firestore

from datetime import datetime

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

@bot.message_handler(commands=["start"])
def start(message):    
    if isVerified(message):
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

        create = types.InlineKeyboardButton("/create")
        list_dir = types.InlineKeyboardButton("/list")
        back = types.InlineKeyboardButton("/back")

        markup.add(create, list_dir, back)

        bot.send_message(
            message.chat.id, 
            f"Heyyy {fetchName(message.chat.id)}! \nWelcome to Nemostyne Admin \nby sh3ldr0id.", 
            reply_markup=markup
        )
        
        retrive()