from app import app
from app.helpers.consts import API_TOKEN, FILES
from app.helpers.getURL import getURL

from flask import redirect

from firebase_admin import firestore

db = firestore.client()

@app.route('/file/<file_id>', methods=['GET'])
def view_file(file_id):
    file_doc = db.collection(FILES).document(file_id).get()

    if not file_doc.exists:
        return redirect("/404")
    
    PATH = getURL(file_doc.get("file_id"))

    if not PATH:
        return redirect("/404")

    return redirect(f'https://api.telegram.org/file/bot{API_TOKEN}/{PATH}')