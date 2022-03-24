from gc import collect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
import json
import pathlib
import pandas as pd
from collection_class import Collection
from NFTProject.back_end.machine_learning.archive_files.preprocess import preprocess
from sklearn.model_selection import train_test_split
from analysis import analyse_results
from NFTProject.back_end.machine_learning.ML_models_functions import random_forest_reg
import pickle
from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict

def reduce_df_most_recent(collection_df):
    # order by timestamp
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
    
collection_dict = retrieve_all_pickles_into_dict()
unique_sorted_dicts = reduce_all_df_most_recent(collection_dict)
set_all_data_to_firebase(unique_sorted_dicts)
