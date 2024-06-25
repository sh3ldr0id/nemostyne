from app import app
from app.helpers.consts import API_TOKEN, FOLDERS, FILES
from app.helpers.folder_location import getLocation
from app.helpers.getURL import getURL

from flask import redirect, render_template

from firebase_admin import firestore

db = firestore.client()

folders_collection = db.collection(FOLDERS)
files_collection = db.collection(FILES)

@app.route('/folder/<folder_id>', methods=['GET'])
def view_folder(folder_id):
    if folder_id == "home":
        folder_id = "Home"
    
    folder_doc = folders_collection.document(folder_id).get()

    if not folder_doc.exists:
        return redirect("/404")
    
    folders = folder_doc.get("folders")
    
    # for folderId in folder_doc.get("folders"):
    #     folder = folders_collection.document(folderId).get()

    #     folders.append({
    #         "id": folder.id,
    #         "name": folder.get("name"),
    #         "created": folder.get("created"),
    #         "folders": len(folder.get("folders")),
    #         "files": len(folder.get("files"))
    #     })

    files = folder_doc.get("files")

    # for fileId in folder_doc.get("files"):
    #     file = files_collection.document(fileId).get()

    #     files.append({
    #         "id": file.id,
    #         "name": file.get("name"),
    #         "created": file.get("created"),
    #     })

    return render_template(
        "folder.html", 
        name=folder_doc.get("name"), 
        locations=getLocation(folder_id), 
        folders=folders, 
        num_folders=len(folders),
        files=files,
        num_files=len(files)
    )