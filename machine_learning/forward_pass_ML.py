from gc import collect
import pickle
from pandas import DataFrame
import pathlib
from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict, retrieve_certain_collection
import firebase_admin
from firebase_admin import db
import numpy as np
import json

# the purpose of this file is to receive a request of a token id and collection
# name from the website, format the appropriate parameters to query a 'what
# would this item sell for now?' question, and return the price, link to image,
# and breakdown of which traits influenced the price

def find_price_predictor_from_tokenid(request):
    cred_push_key = str(pathlib.Path(__file__).resolve().parents[1]) + '/database_store_keys/key_for_ML-prepped-database.json'
    cred_push = firebase_admin.credentials.Certificate(cred_push_key)
    default_app = firebase_admin.initialize_app(cred_push, {
        'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
        })


    # process request
    collection_name = request['collection']
    tokenID = request['tokenid']

    # find model
    filename = str(pathlib.Path(__file__).parent.resolve()) + '/ML_models/random_forests/' + collection_name + "_RF.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))

    # find input
    nft_string = collection_name+tokenID
    print(tokenID)
    ref = db.reference(nft_string)
    data_for_input = ref.get()

    # format input 
    data_for_input_json = DataFrame([data_for_input])
    data_for_input_json = data_for_input_json.drop(['NameOfCollection', 'ethprice', 'tokenID'], axis=1)
    data_for_input_json['timestamp'] = 0


    print(data_for_input)
    print(data_for_input_json)

    predicted_price = loaded_model.predict(data_for_input_json)

    # firebase_admin.delete_app(default_app) # there will DEFINITELY be a better way of doing this!!
    
    collection = retrieve_certain_collection(collection_name)
    target_id = tokenID
    target_index = None
    for i in range (20000):
        if collection.token_id_list[i] == str(target_id):
            target_index = i
            break
    # print(collection.id_ipfs_dict)
    #ipfs = collection.id_ipfs_dict[target_index]
    print(collection.metadata_list[3])

    trait_list = collection.trait_list_dict['100']
    print("trait list:",trait_list)
    trait_list_json = json.loads(trait_list)

    for trait in trait_list_json:
        category = trait["trait_type"]
        # print(collection.tokens_df['tokenID'])
        # print(np.int64(tokenID))
        row = collection.tokens_df.loc[collection.tokens_df['tokenID'] == np.int64(tokenID)]
        specific_value = float(row[category])
        trait["rarity"] = specific_value

    print(trait_list_json)

    predicted_price = np.array2string(*predicted_price)
    response = '{"price":"' + predicted_price + '"},{"ipfs":' + ipfs + '},{"attributes":' + str(trait_list_json)
    
    return predicted_price, ipfs, trait_list

request = {"collection":"boredape","tokenid":"100"}
predicted_price, ipfs, trait_list = find_price_predictor_from_tokenid(request)
# print(predicted_price, ipfs, trait_list)
