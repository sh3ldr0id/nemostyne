from app import bot
from app.helpers.constants import MAIN_CHANNEL, OPEN_FOLDER, DELETE, FILE, FOLDER, PAGE

from telebot import types

from firebase_admin import firestore

db = firestore.client()

files_collection = db.collection("files")
folders_collection = db.collection("folders")

def retrive(message, currentFolder="Home", page=1):
    current_folder = folders_collection.document(currentFolder).get()

    if not current_folder.exists:
        bot.reply_to(message, "Folder doesn't exist!")
        return False
    
    bot.send_message(message.chat.id, f"Viewing '{current_folder.get('name')}'")
    
    files = current_folder.get("files")
    folders = current_folder.get("folders")

    start_index = (page - 1) * 5
    end_index = start_index + 5

    page_folders = folders[start_index:end_index]
    page_files = files[start_index:end_index]

    for folderId in page_folders:
        folder = folders_collection.document(folderId).get()

        folder_name = folder.get("name")
        folder_date = folder.get("created")

        markup = types.InlineKeyboardMarkup(row_width=2)

        open_folder = types.InlineKeyboardButton("Open", callback_data=OPEN_FOLDER+folderId)
        delete = types.InlineKeyboardButton("Delete", callback_data=DELETE+FOLDER+f"_{folderId}")
        markup.add(open_folder, delete)

        bot.send_message(
            message.chat.id, 
            f"📁 {folder_name} \n📅 {folder_date.strftime('%Y-%m-%d %H:%M:%S')}", 
            reply_markup=markup
        )

    for fileId in page_files:
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

    if len(folders) > page*5 or len(files) > page*5:
        markup = types.InlineKeyboardMarkup(row_width=1)

        events = types.InlineKeyboardButton("Next Page", callback_data=PAGE+str(page+1))
        markup.add(events)

        total = len(files)/10

        bot.send_message(message.chat.id, f"Page {page} out of {total if type(total) == int else total+1}", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "That's it. :)")

    return True