import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
import json
import pathlib
import pandas as pd
from collection_class import Collection
import pickle

apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'
coolCatsAddressArchive = '0x1a92f7381b9f03921564a437210bb9396471050c'
coolCatsAddress = '0x1A92f7381B9F03921564a437210bB9396471050C'
cryptoPunkAddress = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
# cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'
cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'
crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'
pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'

#readd punks
list_of_names = ["boredape", "boredapekennel", "clonex", "coolcat", "cryptoad", "doodle", "penguin", "punk"]
collection_name_dict = {'boredape': apeAddress, "boredapekennel": boredApeKennelAddress, "clonex": cloneXAddress,
    "coolcat": coolCatsAddress, "cryptoad": crypToadzAddress, "doodle": doodlesAddress,
    "penguin": pudgyPenguinAddress, "punk": cryptoPunkAddress}

# CREATE LINK FOR 'FULL DATABASE'

cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_ML-prepped-database.json'
cred_push = firebase_admin.credentials.Certificate(cred_push_key)
default_app = firebase_admin.initialize_app(cred_push, {
    'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
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


def prep_individual_collection_data(address, collection_name, next_collection_name):
    ref = db.reference('/', app=tokens_app)
    if next_collection_name == None:
        return
        collection_tokens = ref.order_by_key().start_at(collection_name).get()
    else:
        collection_tokens = ref.order_by_key().start_at(collection_name).end_at(next_collection_name).get()
    ref = db.reference('/', app=transactions_app)
    collection_trans = ref.order_by_child('contracthash').equal_to(address).get()
    # print(collection_tokens)
    collection = Collection(collection_tokens, collection_trans)
    collection.prep_data()
    if collection_name == 'cryptoad':
        collection.price_predict_archive_df = collection.price_predict_archive_df.drop('# Traits', 1)
    return collection
    

def prep_all_collection_data(list_of_names, collection_address_dict):
    list_length = len(list_of_names)
    collection_dict = {}
    for i, name in enumerate(list_of_names):
        address = collection_address_dict[name]
        if (i == list_length - 1):
            collection = prep_individual_collection_data(address, name, None)    
        else:
            collection = prep_individual_collection_data(address, name, list_of_names[i+1])
        collection_dict.update({name: collection})
    return collection_dict

collection_dict = prep_all_collection_data(list_of_names, collection_name_dict)

for name, collection in collection_dict.items():
    with open(str(pathlib.Path(__file__).parent.resolve()) + 
        '/collections_pkl_folder/' + name +
        '_collection_class.pkl', 'wb') as handle:
            pickle.dump(collection, handle)

