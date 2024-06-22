from app import bot

from firebase_admin import firestore
from firebase_admin.firestore import FieldFilter

import re

db = firestore.client()

folders_collection = db.collection("folders")

reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}

def sanitize(message, current_folder_id):
    name = message.text.strip()
    
    if re.search(r'[<>:"/\\|?*]', name):
        bot.reply_to(message, f"'{name}' contains invalid characters. Please pick another name!")
        return False

    if not name:
        bot.reply_to(message, "Name cannot be empty!")
        return False

    if name.upper() in reserved_names:
        bot.reply_to(message, f"'{name}' is not allowed. Please pick another name!")
        return False

    if folders_collection.where(filter=FieldFilter("previous", "==", current_folder_id)).where(filter=FieldFilter("name", "==", name)).get():
        bot.reply_to(message, f"'{name}' already exists. Please pick another name!")
        return False

    return name