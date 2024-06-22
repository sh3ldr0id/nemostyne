from app import bot
from firebase_admin import firestore

db = firestore.client()

users_collection = db.collection("users")

def isVerified(message):
    user = users_collection.document(str(message.chat.id)).get()
    
    if user.exists:
        try:
            if not user.get("verified"):
                bot.send_message(message.chat.id, f"Please ask an Admin to verify your ID ({message.chat.id}).")
                return False
            
        except KeyError:
            bot.send_message(message.chat.id, f"Please ask an Admin to verify your ID ({message.chat.id}).")
            return False
        
    else:
        bot.send_message(message.chat.id, f"Please ask an Admin to verify your ID ({message.chat.id}).")
        return False
    
    return user