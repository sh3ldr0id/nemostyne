from app import bot
from app.helpers.verified import isVerified
from app.helpers.constants import TOKEN, CHANNELS

from firebase_admin import firestore

import subprocess
from PIL import Image
from io import BytesIO
from requests import get
from os import remove
from uuid import uuid4

from datetime import datetime

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

ALLOWED_FILES = ['document', 'photo', 'video', 'audio', 'voice']

@bot.message_handler(content_types=ALLOWED_FILES)
def upload_files(message):
    user = users_collection.document(str(message.chat.id)).get()

    if not isVerified(message):
        return
    
    if message.content_type != "document":
        bot.reply_to(message, "Please send it as documents to save.")
        return

    file_name = message.document.file_name
    file_ext = file_name.split(".")[-1].lower()
    file_id = message.document.file_id
    file_size = message.document.file_size

    thumb_io = None

    try:
        if file_ext in ["jpg", "jpeg", "png"] and file_size <= 15 * 1024 * 1024:
            file_path = bot.get_file(file_id).file_path
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            response = get(file_url)
            
            image = Image.open(BytesIO(response.content))
            image.thumbnail((256, 256))
            thumb_io = BytesIO()
            thumb_io.name = 'thumbnail.jpg'
            image.save(thumb_io, 'JPEG')
            thumb_io.seek(0)

        elif file_ext in ['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm']:
            file_path = bot.get_file(file_id).file_path
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

            thumbnail_path = f"/tmp/{uuid4()}.jpg"
            command = [
                "ffmpeg", "-i", file_url, "-vf", "thumbnail,scale=256:256", "-frames:v", "1", thumbnail_path
            ]

            subprocess.run(command, check=True)

            with open(thumbnail_path, "rb") as f:
                thumb_io = BytesIO(f.read())

            thumb_io.name = 'thumbnail.jpg'

            remove(thumbnail_path)
            
    except:
        thumb_io = None

    thumbnail_file_id = None

    for channel in CHANNELS:
        message_id = bot.forward_message(channel, message.chat.id, message.message_id).message_id
        
        if thumb_io:
            thumbnail_file_id = bot.send_document(channel, thumb_io, reply_to_message_id=message_id).document.file_id
            thumb_io.seek(0)

    current_folder_id = user.get("current")
    current_folder = folders_collection.document(current_folder_id)

    file_id = files_collection.add({
        "owner": str(message.chat.id),
        "previous": current_folder_id,
        "name": file_name,
        "created": datetime.now(),
        "file_id": file_id,
        "thumbnail_file_id": thumbnail_file_id
    })[1].id

    current_folder.update({"files": firestore.ArrayUnion([file_id])})

    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, f"'{file_name}' saved successfully!")