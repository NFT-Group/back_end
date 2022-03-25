from flask import Flask, request
from flask_cors import CORS
import sklearn
import pandas as pd
import numpy as np
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
import time
from datetime import datetime

app = Flask(__name__)

CORS(app)

apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'
coolCatsAddressArchive = '0x1a92f7381b9f03921564a437210bb9396471050c'
coolCatsAddress = '0x1A92f7381B9F03921564a437210bB9396471050C'
cryptoPunkAddress = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'
crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'
pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'

cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + '/machine_learning/database_store_keys/key_for_ML-prepped-database.json'
cred_push = firebase_admin.credentials.Certificate(cred_push_key)
cred_pull_transactions_key = str(pathlib.Path(__file__).parent.resolve()) + '/machine_learning/database_store_keys/key_for_all_transactions_store.json'
cred_pull_transactions = firebase_admin.credentials.Certificate(cred_pull_transactions_key)
try:
    default_app = firebase_admin.initialize_app(cred_push, {
        'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
    })
except:
    a = cred_push

try:
    transactions_app = firebase_admin.initialize_app(cred_pull_transactions, {
        'databaseURL':'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
    }, name='transactions_app')
except:
    a = cred_pull_transactions

@app.route("/", methods=["GET", "POST"])
def index():

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
    ipfs = collection.id_ipfs_dict[tokenID]
    trait_list = collection.trait_list_dict[tokenID]
    trait_list_json = json.loads(trait_list)

    for trait in trait_list_json:
        category = trait["trait_type"]
        row = collection.tokens_df.loc[collection.tokens_df['tokenID'] == np.int64(tokenID)]
        specific_value = float(row[category])
        trait["rarity"] = specific_value

    predicted_price = np.array2string(*predicted_price)
    # doesn't quite work
    if (ipfs[0:4] == "ipfs"):
        ipfs = "https://ipfs.io/ipfs/" + ipfs[7:]


    response = '{"price":"' + predicted_price + '"},{"ipfs":' + ipfs + '},{"attributes":' + str(trait_list_json)

    # return ("We predict that NFT is worth " + predicted_price + "ETH at this exact moment - wow!")
    return response

@app.route("/get_line_graph_data", methods=["GET", "POST"])
def get_line_graph_data():
    data = request.data
    data = json.loads(data)
    timeframe = data['timeframe']
    
    list_of_names = ["boredape", "boredapekennel", "clonex", "coolcat", "cryptoad", "doodle", "penguin", "punk"]
    collection_name_dict = {'boredape': apeAddress, "boredapekennel": boredApeKennelAddress, "clonex": cloneXAddress, "coolcat": coolCatsAddress, "cryptoad": crypToadzAddress, "doodle": doodlesAddress, "penguin": pudgyPenguinAddress, "punk": cryptoPunkAddress}

    if (timeframe == 'day'):
        timeframe = 86400
    elif (timeframe == 'week'):
        timeframe = 604800
    elif (timeframe == 'month'):
        timeframe = 2678400
    elif (timeframe == 'year'):
        timeframe = 31556952
    
    start_time = time.time () - timeframe

    start_time = datetime.utcfromtimestamp(int(start_time)).strftime('%Y-%m-%d')

    ref = db.reference('/', app=transactions_app)
    dates = pd.DataFrame(pd.date_range(start_time, freq="D", periods=(timeframe / 86400)))
    dates = dates.rename(columns={0: 'timestamp'})

    all_trans = ref.order_by_child('timestamp').start_at(start_time).get()

    for i, name in enumerate(list_of_names):
        address = collection_name_dict[name]
        #collection_trans = ref.order_by_child('contracthash').equal_to(address).get()
        collection_df = pd.DataFrame.from_dict(all_trans, orient="index")
        collection_df = collection_df[collection_df.fromaddress != '0x0000000000000000000000000000000000000000']
        collection_df = collection_df[collection_df.ethprice != 0]

        # REMOVE COLUMNS WHICH WON'T BE USED IN PRICE PREDICTION
        collection_df = collection_df.drop([
            'tokenid',
            'fromaddress', 
            'toaddress',
            'tokenuri',
            'transactionhash',
            'blocknumber',
            ], axis=1)
        collection_df_copy = collection_df
        # delete first, redundant column
        collection_df_copy = collection_df_copy.iloc[:,0:]

        collection_df_copy = collection_df_copy.drop(collection_df_copy[collection_df_copy['contracthash'] != address].index)

        # get the last year's data
        collection_df_copy = collection_df_copy.groupby('timestamp', as_index=False)['ethprice'].mean()

        #collection_df = collection_df.drop(collection_df[collection_df.timestamp < one_year_ago].index)

        collection_df_copy = collection_df_copy.rename(columns={'ethprice': name})
        
        # change data type to timestamp so we can compare
        collection_df_copy['timestamp'] = pd.to_datetime(collection_df_copy['timestamp'], format='%Y-%m-%d')

        dates = dates.merge(collection_df_copy, on='timestamp', how='left')
        dates = dates.fillna(method='ffill')
        dates = dates.fillna(0)

    dates['timestamp'] = dates['timestamp'].dt.strftime("%Y-%m-%d")

    retval = dates.to_json(orient='records')
    return retval

