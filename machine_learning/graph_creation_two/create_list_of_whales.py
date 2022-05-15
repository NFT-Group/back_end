import numpy as np
from numpy import genfromtxt
import pandas as pd
from ens import ENS 
from web3 import Web3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# from trait_distribution import trait_distribution 
import json
import pathlib
import pickle
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict




def create_node_graph_data(transactions, jsn_output_name):
    # transactions = pd.read_pickle(pkl_file_name)
    transactions.sort_values("running_whale_weight", ascending = False, inplace = True)

    top_transactions = transactions['fromaddress'].unique()

    top_transactions = top_transactions[0:200]

    buyers_from_top_seller_list = []


    for seller_id in top_transactions:
        temp = transactions.loc[transactions['fromaddress'] == seller_id, 'toaddress']
        buyers_from_top_seller_list.append(temp.tolist())


    buyers_from_top_seller_list = [address for sublist in buyers_from_top_seller_list for address in sublist]
    df = pd.DataFrame(buyers_from_top_seller_list)

    df.to_csv('shows.csv')    
    intersection = np.intersect1d(top_transactions, buyers_from_top_seller_list)
    # collection_data = ref.order_b
    whale_transactions = []

    for line_number, (index, row) in enumerate(transactions.iterrows()):
        if ((row.fromaddress in intersection) and (row.toaddress in intersection)):
            whale_transactions.append(transactions.iloc[[line_number]])

    whale_transactions = pd.concat(whale_transactions)
    f = open(jsn_output_name, 'w')
    f.write("[\n")
    counter = 0
    counter2 = 0
    for sellers_id in intersection:
        name_of_seller = find_wallet_name(sellers_id)
        f.write('{"name":"transactions.' + name_of_seller + '","size":1,"imports":[')
        begin = True
        for index, row in whale_transactions.iterrows():
            counter2 += 1
            # print(row.fromaddress)
            # print(seller_id)
            if(row.fromaddress == sellers_id):
                name_of_buyer = find_wallet_name(row.toaddress)
                if(begin):
                    f.write('"transactions.' + name_of_buyer + '"')
                    counter = counter + 1
                    begin = False
                else:
                    f.write(',"transactions.' + name_of_buyer + '"')
                    counter = counter + 1
        f.write(']},\n')
    f.write("]")


def find_wallet_name(name):
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/28b465e090554529bb7913d0504a71bd'))
    # print(web3.isConnected())
    ns = ENS.fromWeb3(web3)
    try:
        wallet_name = ns.name(name)
        if(wallet_name == None):
            wallet_name = name
        else:
            wallet_name = wallet_name.replace(".", "_")
    except:
        wallet_name = name
        print("error")
    # print(wallet_name)
    return wallet_name



# apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
# # cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
# doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'
# coolCatsAddress = '0x1a92f7381b9f03921564a437210bb9396471050c'
# cryptoPunkAddress = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
# cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'
# cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'
# crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
# boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'
# pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'

# collection_addresses_dict = {'apeAddress': apeAddress, "doodlesAddress": doodlesAddress,
#         "coolCatsAddress": coolCatsAddress,
#         "cloneXAddress": cloneXAddress, "crypToadzAddress": crypToadzAddress,
#         "boredApeKennelAddress": boredApeKennelAddress, "pudgyPenguinAddress": pudgyPenguinAddress}

# # Generate pkl and json files 
# list_pkl_filename = ['cool_cats.pkl', 'bored_ape.pkl', 'doodles.pkl', 'crypto_punks.pkl', 'cloneXAddress.pkl', 'cryptokitties.pkl', 'crypToadzAddress.pkl', 'boredApeKennelAddress.pkl', 'pudgyPenguinAddress.pkl']
#list_json_output_name = ['cool_cats.json', 'bored_ape_yacht_club.json', 'doodles.json', 'crypto_punks.json', 'cloneX.json', 'cryptokitties.json', 'cryptoadz.json', 'bored_ape_kennel_club.json', 'pudgy_penguins.json']
# list_address = [coolCatsAddress, apeAddress, doodlesAddress, cloneXAddress, cryptoKittiesAddress, crypToadzAddress, boredApeKennelAddress, pudgyPenguinAddress]

collection_dict = retrieve_all_pickles_into_dict()
for name, collection in collection_dict.items():
    transactions_df = collection.transactions_df
    create_node_graph_data(transactions_df, name+ '.json')
    print('Written', name)

# for i in range(len(list_pkl_filename)):
#     get_firebase_data_return_pkl_file(list_pkl_filename[i], list_address[i])
    


# #BORED APE DATA
# pkl_file_name = "bored_ape.pkl"
# jsn_output_name = "whale_transactions_bored_ape_node_graph.json"
# address = apeAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_tokens_key = '/database_store_keys/key_for_all_tokens_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)


# #COOLCATS DATA

# pkl_file_name = "cool_cats.pkl"
# jsn_output_name = "whale_transactions_cool_cats_node_graph.json"
# address = coolCatsAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

# #Doodles

# pkl_file_name = "doodles.pkl"
# jsn_output_name = "whale_transactions_doodles_node_graph.json"
# address = doodlesAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_tokens_key = '/database_store_keys/key_for_all_tokens_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

#Cryptopunks DATA

# pkl_file_name = "crypto_punks.pkl"
# jsn_output_name = "whale_transactions_crypto_punks_node_graph.json"
# address = cryptoPunkAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_tokens_key = '/database_store_keys/key_for_all_tokens_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

#cloneXAddress DATA

# pkl_file_name = "cloneXAddress.pkl"
# jsn_output_name = "whale_transactions_cloneXAddress_node_graph.json"
# address = cloneXAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

# #Cryptokitties

# pkl_file_name = "cryptokitties.pkl"
# jsn_output_name = "whale_transactions_cryptokitties_node_graph.json"
# address = cryptoKittiesAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_tokens_key = '/database_store_keys/key_for_all_tokens_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

# #Cryptopunks DATA

# pkl_file_name = "crypToadzAddress.pkl"
# jsn_output_name = "whale_transactions_crypToadzAddress_node_graph.json"
# address = crypToadzAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_tokens_key = '/database_store_keys/key_for_all_tokens_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

# #boredApeKennelAddress DATA

# pkl_file_name = "boredApeKennelAddress.pkl"
# jsn_output_name = "whale_transactions_boredApeKennelAddress_node_graph.json"
# address = boredApeKennelAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)

# #Cryptokitties

# pkl_file_name = "pudgyPenguinAddress.pkl"
# jsn_output_name = "whale_transactions_pudgyPenguinAddress_node_graph.json"
# address = pudgyPenguinAddress
# full_database_key = '/database_store_keys/key_for_full_database_store.json'
# all_tokens_key = '/database_store_keys/key_for_all_tokens_store.json'
# all_transactions_key = '/database_store_keys/key_for_all_transactions_store.json'

# get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key)
# create_node_graph_data(pkl_file_name, jsn_output_name)
