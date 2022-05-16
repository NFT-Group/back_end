from gc import collect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
import json
import pathlib
import pandas as pd
from collection_class import Collection
from sklearn.model_selection import train_test_split
from analysis import analyse_results
from ML_models_functions import random_forest_reg
import pickle
from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict, retrieve_certain_collection

# the purpose of this file is create a reduced version of the transactions
# dataframe which only carries the most recent transactions of each item.
# In this way, we know the 'current' sell count and whale weight so that we
# can accurately predict this price with our model. Once found, we set this
# information to another database so that it can be queried when necessary

cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_ML-prepped-database.json'
cred_push = firebase_admin.credentials.Certificate(cred_push_key)
default_app = firebase_admin.initialize_app(cred_push, {
    'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
    })

def reduce_df_most_recent(collection_df):
    # order by timestamp
    collection_df.timestamp = pd.to_datetime(
        collection_df.timestamp)
    sorted_df = collection_df.sort_values('timestamp', ascending = True)
    uniq_sorted_df = sorted_df.drop_duplicates(subset=['tokenID'], keep='first')
    return uniq_sorted_df

def reduce_all_df_most_recent(collection_dict):
    unique_sorted_dicts = {}
    for name, collection in collection_dict.items():
        if name == 'punk':
            continue
        uniq_sorted_df = reduce_df_most_recent(collection.price_predict_archive_df)
        unique_sorted_dicts.update({name: uniq_sorted_df})
    return unique_sorted_dicts

def set_data_to_firebase(name, collection_df):
    collection_df.insert(0, 'NameOfCollection', name)
    trial_json = collection_df.to_json(orient='records')
    parsed_trial = json.loads(trial_json)
    ref = db.reference('/')
    count = 0
    for row in range(len(parsed_trial)):
        hash = name + str(parsed_trial[row]['tokenID'])
        try:
            ref.child(hash).set(parsed_trial[row])
        except:
            print(hash)
            count = count + 1
    print("Error count is ", count)

def set_all_data_to_firebase(collections_dict):
    for name, collection in collections_dict.items():
        set_data_to_firebase(name, collection)

# MAIN 

# clonex = retrieve_certain_collection('clonex')
# unique_sorted = reduce_df_most_recent(clonex.price_predict_archive_df)
# # set_data_to_firebase('clonex', unique_sorted)
# print(unique_sorted)
    
collection_dict = retrieve_all_pickles_into_dict()
unique_sorted_dicts = reduce_all_df_most_recent(collection_dict)
set_all_data_to_firebase(unique_sorted_dicts)
