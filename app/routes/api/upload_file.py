from app import app, bot
from app.helpers.verifyToken import isVerified
from app.helpers.consts import CHANNELS

from flask import session, request, jsonify

@app.route('/new/file', methods=['POST'])
def upload():
    token = session.get("token")

    if not isVerified(token):
        return jsonify(success=False, error="Unverified")

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

    return jsonify(success=False, error="Empty file")