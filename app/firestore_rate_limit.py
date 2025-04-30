import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase Admin if not already
if not firebase_admin._apps:
    cred = credentials.Certificate('firebaseadminsdk.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def check_and_increment_usage(user_id, tool_name, limit=10, window_seconds=60):
    doc_ref = db.collection('tool_usage').document(f'{user_id}_{tool_name}')
    doc = doc_ref.get()
    now = int(time.time())
    if doc.exists:
        data = doc.to_dict()
        count = data.get('count', 0)
        last_reset = data.get('last_reset', now)
        if now - last_reset < window_seconds:
            if count >= limit:
                return False  # Rate limit exceeded
            else:
                doc_ref.update({'count': count + 1})
                return True
        else:
            doc_ref.set({'count': 1, 'last_reset': now})
            return True
    else:
        doc_ref.set({'count': 1, 'last_reset': now})
        return True
