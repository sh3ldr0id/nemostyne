from app import app
from app.helpers.consts import FILES

from flask import redirect

from firebase_admin import firestore

db = firestore.client()

@app.route('/file/<file_id:str>', methods=['GET'])
def view_file(file_id):
    file_doc = db.collection(FILES).document(file_id).get()

    if not file_doc.exists:
        return redirect("/404")

    return file_id