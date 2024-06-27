from app import app
from app.helpers.consts import API_TOKEN, FOLDERS, FILES

from flask import redirect, render_template

from firebase_admin import firestore

db = firestore.client()

folders_collection = db.collection(FOLDERS)
files_collection = db.collection(FILES)

@app.route('/', methods=['GET'])
def home():
    return redirect("/folder/home")

@app.errorhandler(404)
def not_found(e):
    return "Invalid/Broken URL"

from app.routes import view_folder, view_file, view_thumbnail