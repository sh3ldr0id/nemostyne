from app import app, bot
from app.helpers.verifyToken import isVerified
from app.helpers.sanitize import sanitize
from app.helpers.consts import CHANNELS, FOLDERS, FILES

from flask import session, request, jsonify

from firebase_admin import firestore

db = firestore.client()

folders_collection = db.collection(FOLDERS)
files_collection = db.collection(FILES)

@app.route('/new/folder', methods=['POST'])
def create_folder():
    token = session.get("token")

    if not isVerified(token):
        return jsonify(success=False, error="Unverified")
    
    data = request.json

    name = data["name"]
    
    sanitized = sanitize(name)

    if not sanitized["sucess"]:
        return name
    
    name = sanitized["name"]

    current_folder = folders_collection.document(current_folder_id)

    folder_id = folders_collection.add({
        "previous": current_folder_id,
        "name": name,
        "files": [],
        "folders": [],
        "created": datetime.now(),
        "by": str(message.chat.id)
    })[1].id

    current_folder.update({"folders": firestore.ArrayUnion([folder_id])})

if 'file' not in request.files:
    return jsonify(success=False, error="No file(s) provided")

file = request.files['file']

if file.filename == '':
    return jsonify(success=False, error="No file(s) provided")

if file:
    file_stream = file.stream

    for channel_id in CHANNELS:
        bot.send_document(channel_id, file_stream, visible_file_name=file.filename)
        
        # if thumb_io:
        #     thumbnail_file_id = bot.send_document(channel, thumb_io, reply_to_message_id=message_id).document.file_id
        #     thumb_io.seek(0)
    

    return jsonify(success=True)