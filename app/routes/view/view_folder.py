from app import app
from app.helpers.consts import FOLDERS, FILES

from flask import redirect, render_template

from firebase_admin import firestore

db = firestore.client()

folders_collection = db.collection(FOLDERS)
files_collection = db.collection(FILES)

@app.route('/folder/<folder_id>', methods=['GET'])
def view_folder(folder_id):
    folder_doc = folders_collection.document(folder_id).get()

    if not folder_doc.exists:
        return redirect("/404")
    
    data = folder_doc.to_dict()
    
    folders = data["folders"] if "folders" in data else []
    files = data["files"] if "files" in data else []

    return render_template(
        "folder.html",
        name=folder_doc.get("name"), 
        folders=folders, 
        files=files
    )