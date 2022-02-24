import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
from trait_distribution import trait_distribution 
import json
import pathlib

# CREATE LINK FOR 'FULL DATABASE'

cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_full_database_store.json'
cred_push = firebase_admin.credentials.Certificate(cred_push_key)
default_app = firebase_admin.initialize_app(cred_push, {
    'databaseURL':'https://full-database-9c028-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# CREATE LINK FOR 'ALL TOKENS' DATABASE

cred_pull_tokens_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_tokens_store.json'
cred_pull_tokens = firebase_admin.credentials.Certificate(cred_pull_tokens_key)
tokens_app = firebase_admin.initialize_app(cred_pull_tokens, {
    'databaseURL':'https://alltokens-8ff48-default-rtdb.europe-west1.firebasedatabase.app/'
    }, name = 'tokens_app')

# CREATE LINK FOR 'ALL TRANSACTIONS' DATABASE

cred_pull_transactions_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_transactions_store.json'
cred_pull_transactions = firebase_admin.credentials.Certificate(cred_pull_transactions_key)
transactions_app = firebase_admin.initialize_app(cred_pull_transactions, {
    'databaseURL':'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
    }, name='transactions_app')

# ref = tokens_app.reference('/')
ref = db.reference('/', app=tokens_app)

bored_apes = ref.order_by_key().start_at('boredape').end_at('boredapekennel').get()
# bored_apes_list = list(bored_apes.items())

id_list = []
metadata_list = []

for id, meta in bored_apes.items():
    id_temp = json.dumps(meta["tokenid"])
    id_list.append(id_temp)
    metadata_temp = json.dumps(meta["metadata"])
    metadata_temp = metadata_temp.replace("\\","")[1:-1]
    metadata_temp = json.loads(metadata_temp)
    metadata_temp = json.dumps(metadata_temp["attributes"])
    metadata_list.append(metadata_temp)   

print(metadata_list)

unique_header_list, trait_values_distribution = trait_distribution(id_list, metadata_list)

print(unique_header_list)
print(trait_values_distribution)

# print(unique_header_list)
# print(trait_values_distribution)



