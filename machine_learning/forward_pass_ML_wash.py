from gc import collect
import pickle
from xml.etree.ElementPath import prepare_child
from pandas import DataFrame
import pathlib
from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict, retrieve_certain_collection
import firebase_admin
from firebase_admin import db
from ML_models_functions import random_forest_reg
from sklearn.model_selection import train_test_split
from analysis import analyse_results
import numpy as np
import json

list_of_names = ["boredape", "boredapekennel", "clonex", "coolcat", "cryptoad", "doodle", "penguin", "punk"]

def retrieve_collection_dodgies(name):
    with open(str(pathlib.Path(__file__).parent.resolve()) + 
        '/creating_node_graph/list_of_dodgy_transactions/' + name +
        '.pkl', 'rb') as f:
           data = pickle.load(f)
    return data

def retrieve_certain_collection(name):
    with open(str(pathlib.Path(__file__).parent.resolve()) + 
        '/collections_pkl_folder/' + name +
        '_collection_class.pkl', 'rb') as f:
           data = pickle.load(f)
    return data

def find_price_predictor_from_transactionhashes(collection_name, dodgy_transactions):

    print("-------------------------- " + collection_name + " ------------------------------")

    try:
        cred_push_key = str(pathlib.Path(__file__).resolve().parents[1]) + '/database_store_keys/key_for_ML-prepped-database.json'
        cred_push = firebase_admin.credentials.Certificate(cred_push_key)
        default_app = firebase_admin.initialize_app(cred_push, {
            'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
            })
    except: 
        a = 1

    collection = retrieve_certain_collection(collection_name)
    preprocessed_df = collection.preprocessed_df
    preprocessed_df2 = preprocessed_df

    for hash in dodgy_transactions:
        if(hash != 'start loop'):
            row_in_question = collection.transactions_df.loc[collection.transactions_df['transactionhash'] == hash]
            tokenID = row_in_question['tokenid'].values[0]
            eth_price = row_in_question['ethprice'].values[0]
            preprocessed_df = preprocessed_df[(preprocessed_df.tokenID != tokenID) | (preprocessed_df.ethprice != eth_price)]

    x = preprocessed_df.drop(['ethprice', 'tokenID'], axis=1)
    if(collection_name == 'cryptoad'):
        x = x.drop(['# Traits'], axis =1)
    x = x.sort_index(axis=1, ascending=True) # IMPORTANT LINE TO ENSURE LINEUP
    y = preprocessed_df['ethprice']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, shuffle=True)
    y_pred, y_test, model = random_forest_reg(x_train, x_test, y_train, y_test)


    actual_cost_total = 0
    predicted_cost_total = 0
    count = 0
    for hash in dodgy_transactions:
        if(hash != 'start loop'):
            row_in_question = collection.transactions_df.loc[collection.transactions_df['transactionhash'] == hash]
            tokenID = row_in_question['tokenid'].values[0]
            eth_price = row_in_question['ethprice'].values[0]
            actual_cost_total += eth_price
            try:    
                timestamp_for_later = preprocessed_df2.timestamp[
                    (preprocessed_df2.tokenID == tokenID) & (preprocessed_df2.ethprice == eth_price)].values[0]
                whale_weight_for_later = preprocessed_df2.running_whale_weight[
                    (preprocessed_df2.tokenID == tokenID) & (preprocessed_df2.ethprice == eth_price)].values[0]
                sell_count_for_later = preprocessed_df2.running_sell_count[
                    (preprocessed_df2.tokenID == tokenID) & (preprocessed_df2.ethprice == eth_price)].values[0]
                nft_string = collection_name+str(tokenID)
                ref = db.reference(nft_string)
                data_for_input = ref.get()

                data_for_input_json = DataFrame([data_for_input])
                data_for_input_json = data_for_input_json.drop(['NameOfCollection', 'ethprice', 'tokenID'], axis=1)
                data_for_input_json['timestamp'] = timestamp_for_later
                data_for_input_json['running_sell_count'] = sell_count_for_later
                data_for_input_json['running_whale_weight'] = whale_weight_for_later

                predicted_price = model.predict(data_for_input_json)
                # print("what it should have cost:")
                # print(predicted_price)
                predicted_cost_total += predicted_price
                if(eth_price > predicted_price + 3):
                    print("Actual price " + str(eth_price) + " and predicted price " + str(predicted_price) )
                # if(predicted_price > eth_price + 10):
                #     print("Actual price" + str(eth_price) + " and predicted price " + str(predicted_price) )
                # print("\n")
            except:
                print(row_in_question)


    print("Actual cost")
    print(actual_cost_total)
    print("Predicted price")
    print(predicted_cost_total)




for name in list_of_names:
    dodgies = retrieve_collection_dodgies(name)
    find_price_predictor_from_transactionhashes(name, dodgies)

# collection_dict = retrieve_all_pickles_into_dict()
# for name, collection in collection_dict.items():
#     print(name) 
#     find_price_predictor_from_transactionhashes('boredape',bored_apes_dodgies)

#     find_price_predictor_from_transactionhashes(name,collection)


# bored_apes_dodgies = retrieve_collection_dodgies('boredape')




# print("average is: ", total/count)


# request = {"collection":"boredape","tokenid":"1000","timestamp":400000}
# predicted_price, ipfs, trait_list = find_price_predictor_from_tokenid(request)
# print(predicted_price, ipfs, trait_list)
