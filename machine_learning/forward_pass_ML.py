from gc import collect
import pickle
from pandas import DataFrame
import pathlib
from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict, retrieve_certain_collection
import firebase_admin
from firebase_admin import db

def find_price_predictor_from_tokenid(request):
    cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_ML-prepped-database.json'
    cred_push = firebase_admin.credentials.Certificate(cred_push_key)
    default_app = firebase_admin.initialize_app(cred_push, {
        'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/'
        })

    # process request
    collection_name = request['collection']
    tokenID = request['tokenid']

    # find model - THIS WILL LIKELY NEED TO BE CHANGED
    filename = str(pathlib.Path(__file__).parent.resolve()) + '/ML_models/random_forests/' + collection_name + "_RF.pkl"

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

    # firebase_admin.delete_app(default_app) # there will DEFINITELY be a better way of doing this!!
    
    collection = retrieve_certain_collection(collection_name)
    ipfs = collection.id_ipfs_dict[tokenID]
    trait_list = collection.trait_list_dict[tokenID]

    print(type(predicted_price))
    # trait_list = collection_dict[collection_name].metadatalist
    response = '{"price":' + str(predicted_price)
    print(response)

    return predicted_price, ipfs, trait_list

request = {"collection":"penguin","tokenid":"345"}
predicted_price, ipfs, trait_list = find_price_predictor_from_tokenid(request)
print(predicted_price, ipfs, trait_list)
