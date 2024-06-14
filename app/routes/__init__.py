from app import app
from app.routes import view_folder, view_file

@app.route('/', methods=['GET'])
def home():
    return "Welcome to home page"

@app.errorhandler(404)
def not_found(e):
    return "Invalid/Broken URL"