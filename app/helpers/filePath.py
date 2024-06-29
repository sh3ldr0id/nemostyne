from app.helpers.consts import API_TOKEN
from requests import get

def getFilePath(file_id):
    response = get(f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}").json()

    if response["ok"]:
        return response["result"]["file_path"]
    
    return False