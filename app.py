from flask import Flask, request
from flask_cors import CORS
import sklearn
import pandas
import pickle
import firebase_admin
from firebase_admin import credentials, firestore, db
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from machine_learning.retrieve_collections_from_pkl import retrieve_all_pickles_into_dict, retrieve_certain_collection

import pathlib
import json
import pickle
import os.path

app = Flask(__name__)

CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + '/machine_learning/database_store_keys/key_for_ML-prepped-database.json'
    cred_push = firebase_admin.credentials.Certificate(cred_push_key)
    try:
        default_app = firebase_admin.initialize_app(cred_push, {
        'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
        })
    except:
        a = cred_push

    data = request.data
    data = json.loads(data)
    collection_name = data['collection']
    tokenID = data['tokenid']

    filename = str(pathlib.Path(__file__).parent.resolve()) + '/machine_learning/ML_models/random_forests/' + collection_name + "_RF.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))

    # find input
    nft_string = collection_name+tokenID
    ref = db.reference(nft_string)
    data_for_input = ref.get()

    # format input 
    data_for_input_json = DataFrame([data_for_input])
    data_for_input_json = data_for_input_json.drop(['NameOfCollection', 'ethprice', 'tokenID'], axis=1)
    data_for_input_json['timestamp'] = 0

    predicted_price = loaded_model.predict(data_for_input_json)

    collection = retrieve_certain_collection(collection_name)
    # ipfs = collection.id_ipfs_dict[tokenID]
    # trait_list = collection.trait_list_dict[tokenID]
    # collection_dict = retrieve_all_pickles_into_dict()
    # ipfs = collection_dict[collection_name].id_ipfs_dict[tokenID]

    return str("We predict that NFT is worth ", predicted_price, " at this exact moment - wow!")
    return str(predicted_price, ipfs, trait_list)

