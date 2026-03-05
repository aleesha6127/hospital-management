import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'hospital-management-809fb.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()
