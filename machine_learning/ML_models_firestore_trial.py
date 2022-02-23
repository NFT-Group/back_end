import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/tm21/Documents/key_for_all_tokens_store")
default_app = firebase_admin.initialize_app(cred, {
    'https://console.firebase.google.com/u/1/project/alltokens-8ff48/database/alltokens-8ff48-default-rtdb/data':all_tokens)
        })

