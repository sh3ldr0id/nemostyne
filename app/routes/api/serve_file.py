from app import app
from app.helpers.filePath import getFilePath
from app.helpers.consts import API_TOKEN, FILES

from flask import redirect, Response
from requests import get

from firebase_admin import firestore

db = firestore.client()

@app.route('/download/<file_id>', methods=['GET'])
def serve_file(file_id):
    file_doc = db.collection(FILES).document(file_id).get()

    if not file_doc.exists:
        return redirect("/404")
    
    PATH = getFilePath(file_doc.get("file_id"))

    if not PATH:
        return redirect("/404")
    
    def generate():
        with get(f'https://api.telegram.org/file/bot{API_TOKEN}/{PATH}', stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    headers = {
        'Content-Disposition': f'attachment; filename="{file_doc.get("name")}"'
    }
    
    return Response(generate(), headers=headers, content_type='application/octet-stream')