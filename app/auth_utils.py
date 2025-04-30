import firebase_admin
from firebase_admin import auth, credentials
from flask import request, jsonify

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('firebaseadminsdk.json')
    firebase_admin.initialize_app(cred)

def get_firebase_uid_from_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, jsonify({'error': 'Missing or invalid Authorization header.'}), 401
    id_token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid'], None, None
    except Exception:
        return None, jsonify({'error': 'Invalid or expired token.'}), 401