import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
from trait_distribution import trait_distribution 
import json
import pathlib
import pandas as pd
from collection_class import Collection

apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
# cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'
coolCatsAddress = '0x1a92f7381b9f03921564a437210bb9396471050c'
# cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'
cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'
crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'
pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'

collection_addresses_dict = {'apeAddress': apeAddress, "doodlesAddress": doodlesAddress,
        "coolCatsAddress": coolCatsAddress,
        "cloneXAddress": cloneXAddress, "crypToadzAddress": crypToadzAddress,
        "boredApeKennelAddress": boredApeKennelAddress, "pudgyPenguinAddress": pudgyPenguinAddress}




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


# JUST ONE BORED APES EXAMPLE FOR NOW BUT CAN MAKE THIS SECTION TRAVERSABLE LATER

ref = db.reference('/', app=tokens_app)
bored_apes_data = ref.order_by_key().start_at('boredape').end_at('boredapekennel').get()
ref = db.reference('/', app=transactions_app)
# bored_apes_trans = ref.order_by_child('contracthash').equal_to(apeAddress).get()
bored_apes_trans = ref.order_by_child('contracthash').equal_to(apeAddress).limit_to_first(5000).get()
bored_apes = Collection(bored_apes_data, bored_apes_trans)
bored_apes.prep_data()

# count_dict = dict((id, 0) for id in list(bored_apes.tokens_df['tokenID']))
# print(count_dict)

