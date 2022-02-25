import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
from trait_distribution import trait_distribution 
import json
import pathlib
import pandas as pd

class Collection:
    trait_header_list = []
    trati_header_list_mod = []
    trait_distribution = []
    tokens_df = pd.DataFrame()
    transactions_headers = []
    raw_transactions_data = []
    transactions_df = pd.DataFrame()

def split_data(tokens_from_collection):
    # initial split of data from an OrderedDict into two lists

    id_list = []
    metadata_list = []

    for id, meta in tokens_from_collection.items():
        id_temp = json.dumps(meta["tokenid"])
        id_list.append(id_temp)
        metadata_temp = json.dumps(meta["metadata"])
        metadata_temp = metadata_temp.replace("\\","")[1:-1]
        metadata_temp = json.loads(metadata_temp)
        metadata_temp = json.dumps(metadata_temp["attributes"])
        metadata_list.append(metadata_temp)  

    return id_list, metadata_list 

def get_raw_transaction_data(transactions_from_collection):
    # initial split of transactions data from ordered dict into a 
    # list of headers and a list of all the raw data without headers

    data_list = []

    for id, other_data in transactions_from_collection.items():
        transaction_hash = json.dumps(id)
        data_temp = json.loads(json.dumps(other_data))
        data_list.append(data_temp)
        transactions_keys = list(data_list[0].keys())
        transactions_values = [list(d.values()) for d in data_list]
    
    return transactions_keys, transactions_values

def sell_count(transactions_data):
        unique_id = OrderedSet(transactions_data[:,-4])
        unique_id = np.array(list(unique_id), dtype=int)
        transactions_data_id_list = np.array(transactions_data[:,-4], dtype=int)
        sell_count_array = np.zeros([len(transactions_data),1])

        count_dict = dict.fromkeys(unique_id, 0)

        for row in range(len(unique_id)):
                for i, j in zip(range(len(transactions_data_id_list)), range(len(sell_count_array))):
                        if(unique_id[row] == transactions_data_id_list[i]):
                                count_dict[unique_id[row]] += 1
                                sell_count_array[i,0] = count_dict[unique_id[row]]
       

        print("SELL COUNT ARRAY: ", sell_count_array)
        return sell_count_array


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

ref = db.reference('/', app=tokens_app)

# JUST ONE BORED APES EXAMPLE FOR NOW BUT CAN MAKE THIS SECTION TRAVERSABLE LATER

bored_apes = Collection()
bored_apes_data = ref.order_by_key().start_at('boredape').end_at('boredapekennel').get()

bored_ape_id_list, bored_ape_metadata_list = split_data(bored_apes_data)
bored_apes_trait_header_list, bored_apes_trait_values_distribution = trait_distribution(bored_ape_id_list, bored_ape_metadata_list)

ref = db.reference('/', app=transactions_app)
bored_apes_trans = ref.order_by_child('contracthash').equal_to(apeAddress).limit_to_first(10).get()
bored_apes_transactions_headers, bored_apes_trans_raw_data = get_raw_transaction_data(bored_apes_trans)

bored_apes.trait_header_list = bored_apes_trait_header_list
bored_apes.trait_header_list_mod = bored_apes.trait_header_list
bored_apes.trait_header_list_mod.insert(0,'tokenID')
bored_apes.trait_header_list_mod.append('NumOfTraits')

bored_apes.trait_distribution = bored_apes_trait_values_distribution
bored_apes.tokens_df = pd.DataFrame(bored_apes.trait_distribution, columns = bored_apes.trait_header_list_mod)
bored_apes.transactions_headers = bored_apes_transactions_headers
bored_apes.raw_transactions_data = bored_apes_trans_raw_data
bored_apes.transactions_df = pd.DataFrame(bored_apes.raw_transactions_data, columns = bored_apes_transactions_headers)

# print(bored_apes.trait_header_list)
# print(bored_apes_trait_values_distribution)
# print(bored_apes.tokens_df)
# print(bored_apes.transactions_headers)
# print(bored_apes.raw_transactions_data)

# ADD SELLER COUNT AND REAL USD PRICE IN A ROBUST AND MOBILE WAY...

count_dict = dict((id, 0) for id in list(bored_apes.tokens_df['tokenID']))

