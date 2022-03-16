import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
import json
import pathlib
import pandas as pd
from collection_class import Collection
from preprocess import preprocess
from sklearn.model_selection import train_test_split
from analysis import analyse_results
from ML_Models import random_forest_reg
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

# collection_addresses_dict = {'apeAddress': apeAddress, "doodlesAddress": doodlesAddress,
#         "coolCatsAddress": coolCatsAddress,
#         "cloneXAddress": cloneXAddress, "crypToadzAddress": crypToadzAddress,
#         "boredApeKennelAddress": boredApeKennelAddress, "pudgyPenguinAddress": pudgyPenguinAddress}

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
        collection.preprocessed_df = collection.preprocessed_df.drop('# Traits', 1)
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
        uniq_sorted_df = reduce_df_most_recent(collection.preprocessed_df)
        unique_sorted_dicts.update({name: uniq_sorted_df})
    return unique_sorted_dicts


def set_data_to_firebase(name, collection_df):
    collection_df.insert(0, 'NameOfCollection', name)
    trial_json = collection_df.to_json(orient='records')
    parsed_trial = json.loads(trial_json)
    ref = db.reference('/')
    for row in range(len(parsed_trial)):
        hash = name + str(parsed_trial[row]['tokenID'])
        ref.child(hash).set(parsed_trial[row])


def set_all_data_to_firebase(collections_dict):
    for name, collection in collections_dict.items():
        set_data_to_firebase(name, collection)
    

# collection_dict = prep_all_collection_data(list_of_names, collection_name_dict)
# print(collection_dict)
# unique_sorted_dicts = reduce_all_df_most_recent(collection_dict)
# set_all_data_to_firebase(unique_sorted_dicts)

# bored_apes = prep_individual_collection_data(apeAddress, 'boredape', 'boredapekennel')
# preprocessed_df = bored_apes.preprocessed_df


preprocessed_df = pd.read_pickle("apes_preprocessed_df.pkl")
x = preprocessed_df.drop(['ethprice'], axis=1)
x = x.sort_index(axis=1, ascending=True)
y = preprocessed_df['ethprice']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, shuffle=False)
y_pred, y_test, model = random_forest_reg(x_train, x_test, y_train, y_test)
print(x_train)
analyse_results(y_pred, y_test, 'BoredApes')

filename = "bored_apes_model.pkl"
pickle.dump(model, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(x_test)
analyse_results(y_pred, y_test, 'BoredApes')

prediction = loaded_model.predict(x)

ref = db.reference('boredape4372')
data_for_input = ref.get()
print(data_for_input)

# data_for_input_json = pd.DataFrame.from_dict(data_for_input, orient="records")
data_for_input_json = pd.DataFrame([data_for_input])

data_for_input_json = data_for_input_json.drop(['NameOfCollection', 'ethprice'], axis=1)
data_for_input_json['timestamp'] = 0
print(data_for_input_json)

price_prediction = loaded_model.predict(data_for_input_json)
print(price_prediction)








# print(preprocessed_df)
# preprocess(prepped_df)

# print(x)
# print(y)



# testable_data = prepped_df.drop([''])


# count_dict = dict((id, 0) for id in list(bored_apes.tokens_df['tokenID']))
# print(count_dict)

# def get_prepped_data(collection_name):
#     cred_pull_tokens_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_tokens_store.json'
# cred_pull_tokens = firebase_admin.credentials.Certificate(cred_pull_tokens_key)
# tokens_app = firebase_admin.initialize_app(cred_pull_tokens, {
#     'databaseURL':'https://alltokens-8ff48-default-rtdb.europe-west1.firebasedatabase.app/'
#     }, name = 'tokens_app')

# # CREATE LINK FOR 'ALL TRANSACTIONS' DATABASE

# cred_pull_transactions_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_transactions_store.json'
# cred_pull_transactions = firebase_admin.credentials.Certificate(cred_pull_transactions_key)
# transactions_app = firebase_admin.initialize_app(cred_pull_transactions, {
#     'databaseURL':'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
#     }, name='transactions_app')
