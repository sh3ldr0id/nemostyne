from app import bot
from app.helpers.verified import isVerified
from app.helpers.retrive import retrive

from firebase_admin import firestore

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

@bot.message_handler(commands=["list"])
def list_dir(message):    
    user = isVerified(message)

    if user:
        current_folder_id = user.get("current")
        retrive(message, current_folder_id)