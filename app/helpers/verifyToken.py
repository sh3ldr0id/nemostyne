from firebase_admin import auth

def isVerified(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        custom_claims = auth.get_user(uid).custom_claims

        if "verified" in custom_claims:
            return True
        
        return False
    
    except Exception as e:
        return False