from firebase_admin import firestore
from firebase_admin.firestore import FieldFilter

import re

db = firestore.client()

folders_collection = db.collection("folders")

reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}

def sanitize(name, current_folder_id):
    name = name.strip()
    
    if re.search(r'[<>:"/\\|?*]', name):
        return {"success": False, "reason": "Invalid"}

    if not name:
        return {"success": False, "reason": "Empty"}

    if name.upper() in reserved_names:
        return {"success": False, "reason": "Reserved"}

    if folders_collection.where(filter=FieldFilter("previous", "==", current_folder_id)).where(filter=FieldFilter("name", "==", name)).get():
        return {"success": False, "reason": "Exists"}

    return {"success": True, "name": name}