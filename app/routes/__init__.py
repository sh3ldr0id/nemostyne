from app import app

from flask import redirect

@app.route('/', methods=['GET'])
def home():
    return redirect("/folder/Home")

@app.errorhandler(404)
def not_found(e):
    return "Invalid/Broken URL"

from app.routes.view import view_folder, view_file
from app.routes.api import verify_token, serve_file