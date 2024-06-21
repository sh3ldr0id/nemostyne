from app import bot
from app.helpers.constants import MAIN_CHANNEL, OPEN_FOLDER, DELETE, FILE, FOLDER

from telebot import types

from firebase_admin import firestore

db = firestore.client()

files_collection = db.collection("files")
folders_collection = db.collection("folders")

def retrive(message, currentFolder="Home"):
    current_folder = folders_collection.document(currentFolder).get()

    if not current_folder.exists:
        bot.reply_to(message, "Folder doesn't exist!")
        return
    
    files = current_folder.get("files")
    folders = current_folder.get("folders")

    for folderId in folders:
        folder = folders_collection.document(folderId).get()

        folder_name = folder.get("name")
        folder_date = folder.get("date")

        markup = types.InlineKeyboardMarkup(row_width=2)

        open_folder = types.InlineKeyboardButton("Open", callback_data=OPEN_FOLDER+folderId)
        delete = types.InlineKeyboardButton("Delete", callback_data=DELETE+FOLDER+f"_{folderId}")
        markup.add(open_folder, delete)

        bot.send_message(
            message.chat.id, 
            f"📁 {folder_name} \n📅 {folder_date.strftime('%Y-%m-%d %H:%M:%S')}", 
            reply_markup=markup
        )

    for fileId in files:
        file = files_collection.document(fileId).get()

        file_name = file.get("name")
        file_date = file.get("date")

        message_id = file.get("main")

        forwarded_message = bot.forward_message(message.chat.id, MAIN_CHANNEL, message_id)

        markup = types.InlineKeyboardMarkup(row_width=1)

        delete = types.InlineKeyboardButton("Delete", callback_data=DELETE+FILE+f"_{fileId}")
        markup.add(delete)

        bot.reply_to(
            forwarded_message, 
            f"📄 {file_name} \n📅 {file_date.strftime('%Y-%m-%d %H:%M:%S')}", 
            reply_markup=markup
        )

    bot.send_message(message.chat.id, "That's it. :)")