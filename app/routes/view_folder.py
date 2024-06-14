from app import app
from app.helpers.consts import FOLDERS

from flask import redirect

from firebase_admin import firestore

db = firestore.client()

@app.route('/folder/<folder_id:str>', methods=['GET'])
def view_folder(folder_id):
    folder_doc = db.collection(FOLDERS).document(folder_id).get()

    if not folder_doc.exists:
        return redirect("/404")