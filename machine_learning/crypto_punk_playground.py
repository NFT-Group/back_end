import firebase_admin 
from firebase_admin import db
import pathlib
from retrieve_collections_from_pkl import retrieve_certain_collection


cred_pull_tokens_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_tokens_store.json'
cred_pull_tokens = firebase_admin.credentials.Certificate(cred_pull_tokens_key)
tokens_app = firebase_admin.initialize_app(cred_pull_tokens, {
    'databaseURL':'https://alltokens-8ff48-default-rtdb.europe-west1.firebasedatabase.app/'
    })


ref = db.reference('/')

collection_tokens = ref.order_by_key().start_at('punk').get()
print(collection_tokens)

bored_apes = retrieve_certain_collection('boredape')
print(bored_apes.trait_list_dict['100'])

