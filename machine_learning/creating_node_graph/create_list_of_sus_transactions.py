import numpy as np
from numpy import genfromtxt
import pandas as pd
from ens import ENS 
from web3 import Web3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pickle
# from trait_distribution import trait_distribution 
import json
import pathlib
from collection_class_lite import Collection_lite



def get_firebase_data_return_pkl_file(pkl_file_name, address, full_database_key, all_transactions_key):

    # CREATE LINK FOR 'FULL DATABASE'

    cred_push_key = str(pathlib.Path(__file__).parent.resolve()) + full_database_key
    cred_push = firebase_admin.credentials.Certificate(cred_push_key)
    default_app = firebase_admin.initialize_app(cred_push, {
        'databaseURL':'https://full-database-9c028-default-rtdb.europe-west1.firebasedatabase.app/'
        })

    # CREATE LINK FOR 'ALL TRANSACTIONS' DATABASE

    cred_pull_transactions_key = str(pathlib.Path(__file__).parent.resolve()) + all_transactions_key
    cred_pull_transactions = firebase_admin.credentials.Certificate(cred_pull_transactions_key)
    transactions_app = firebase_admin.initialize_app(cred_pull_transactions, {
        'databaseURL':'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
        }, name='transactions_app')


    # JUST ONE BORED APES EXAMPLE FOR NOW BUT CAN MAKE THIS SECTION TRAVERSABLE LATER

    ref = db.reference('/', app=transactions_app)
    transactions = ref.order_by_child('contracthash').equal_to(address).get()
    # print(transactions)
    collection = Collection_lite(transactions)
    collection.prep_data()
    print(collection)
    collection.transactions_df.to_pickle(pkl_file_name)


def create_node_graph_data(pkl_file_name, jsn_output_name, pickle_whale_loops):
    transactions = pd.read_pickle(pkl_file_name)
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
    with open (pickle_whale_loops, 'rb') as fp:
        transaction_list1 = pickle.load(fp)
    for sellers_id in intersection:
        name_of_seller = find_wallet_name(sellers_id)
        f.write('{"name":"transactions.' + name_of_seller + '","size":1,"imports":[')
        begin = True
        for index, row in whale_transactions.iterrows():
            counter2 += 1
            if(row.fromaddress == sellers_id):
                if(row.transactionhash in transaction_list1):
                    print(row.transactionhash)
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
    return wallet_name



apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
# cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'
coolCatsAddress = '0x1a92f7381b9f03921564a437210bb9396471050c'
cryptoPunkAddress = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'
cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'
crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'
pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'

collection_addresses_dict = {'apeAddress': apeAddress, "doodlesAddress": doodlesAddress,
        "coolCatsAddress": coolCatsAddress,
        "cloneXAddress": cloneXAddress, "crypToadzAddress": crypToadzAddress,
        "boredApeKennelAddress": boredApeKennelAddress, "pudgyPenguinAddress": pudgyPenguinAddress}

# Make json files 
# list_pkl_whale_loops = ['bored_ape_loops.pkl']
list_pkl_filename = ['boredape_loops.pkl', 'boredapekennel_loops.pkl', 'coolcat_loops.pkl', 'doodle_loops.pkl', 'clonex_loops.pkl', 'cryptoad_loops.pkl', 'penguin_loops.pkl']
list_json_output_name = ['bored_ape_yacht_club_loops.json', 'bored_ape_kennel_club_loops.json', 'cool_cats_loops.json', 'doodles_loops.json', 'clonex_loops.json', 'cryptoadz_loops.json', 'pudgy_penguins_loops.json']
list_address = [apeAddress, boredApeKennelAddress, coolCatsAddress, doodlesAddress, cloneXAddress, crypToadzAddress, pudgyPenguinAddress]
full_database_key = '../database_store_keys/key_for_full_database_store.json'
all_tokens_key = '../database_store_keys/key_for_all_tokens_store.json'
all_transactions_key = '../database_store_keys/key_for_all_transactions_store.json'
for i in range(len(list_pkl_filename)):
    create_node_graph_data(list_pkl_filename[i], list_json_output_name[i], )