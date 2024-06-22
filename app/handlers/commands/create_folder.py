from app import bot
from app.helpers.verified import isVerified

from firebase_admin import firestore

db = firestore.client()

users_collection = db.collection("users")

@bot.message_handler(commands=["create"])
def create_file(message):    
    if isVerified(message):
        user = users_collection.document(str(message.chat.id))

        bot.send_message(message.chat.id, "Sure! I'l create a folder. What do you want to name it?")

        user.update({"listening": "folder_name"})    