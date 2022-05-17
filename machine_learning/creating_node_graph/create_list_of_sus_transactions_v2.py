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
import os
import sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir1 = os.path.dirname(currentdir)
sys.path.insert(0, parentdir1) 

from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict


print("hello")

# get a list of the whales to look at - top 400 
# within those top whales, find a list of all of their buyers
# recursively go through the buyers until the target_address is found and timing is within a month, or the recursion is too high
# if a loop is found, add all of the transaction hashes a list 
# find a long list of all the dodgy transaction hashes 
# with that list add every transaction to the loop graph

# get a list of the whales to look at - top 400 


# put the timestamp into the first find all buyers 
# check that the timestamp is within a month in both the 



def find_all_loops(list_of_whales, transactions_df):
    dodgy_transactions_list = []
    dodgy_transactions_list_time = []
    for whale_address in list_of_whales:
        list_of_addresses_in_loop = []
        list_of_timestamps_in_loop = []
        find_all_buyers(transactions_df, whale_address, whale_address, list_of_addresses_in_loop, list_of_timestamps_in_loop, 0)
        if(len(list_of_addresses_in_loop) != 0):
            dodgy_transactions_list.append(list_of_addresses_in_loop)
            dodgy_transactions_list_time.append(list_of_timestamps_in_loop)
            print(len(dodgy_transactions_list))

    flat_list = [item for sublist in dodgy_transactions_list for item in sublist]
    flat_list_time = [item for sublist in dodgy_transactions_list_time for item in sublist]
    return flat_list, flat_list_time



# find all buyers of a seller, if a buyer is a target address return true and 
# add seller address and whale address to the list of addresses 
def find_all_buyers(transactions_df, whale_address, target_address, list_of_addresses_in_loop, list_of_timestamps_in_loop, count):
    count = count + 1
    if(count > 3):
        return False
    list_of_buyers = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'toaddress'])
    list_of_transactions = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'transactionhash']).tolist()
    list_of_timestamps = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'timestamp']).tolist()
    list_of_buyers = list_of_buyers.tolist()
    found = False
    if(len(list_of_buyers) == 0):
        return False
    for i in range(len(list_of_buyers)):
        if (list_of_buyers[i] == target_address):
            list_of_addresses_in_loop.append("start loop")
            list_of_timestamps_in_loop.append("start loop")
            list_of_addresses_in_loop.append(list_of_transactions[i])
            list_of_timestamps_in_loop.append(list_of_timestamps[i])
            return True
        elif(find_all_buyers(transactions_df, list_of_buyers[i], target_address, list_of_addresses_in_loop, list_of_timestamps_in_loop, count)):
            list_of_addresses_in_loop.append(list_of_transactions[i])
            list_of_timestamps_in_loop.append(list_of_timestamps[i])
            found = True
    if(found):
        return True
    return False




def loop_data():
    collection_dict = retrieve_all_pickles_into_dict()
    for name, collection in collection_dict.items():
            if(collection == None):
                return
            transactions_df = collection.transactions_df
            print(name)
            transactions_df.sort_values("running_whale_weight", ascending = False, inplace = True)
            top_whale_sellers = transactions_df['fromaddress'].unique()
            top_whale_sellers = top_whale_sellers[0:200]
            flat_list, flat_list_time = find_all_loops(top_whale_sellers, transactions_df)
            with open('list_of_dodgy_transactions/' + name +
                '.pkl', 'wb') as f:
                    pickle.dump(flat_list, f)
                    print("Created")
            with open('list_of_dodgy_transactions/' + name +
                '.pkl', 'wb') as ft:
                    pickle.dump(flat_list, ft)
                    print("Created")
            print(flat_list)
            print(flat_list_time)


# This will rerun all of the loop data - creating a list of transaction hashes of dodgy transactions (loops), 
# where the "to address" in the first transaction after 'start loop' and the 'from address' in the last transaction hash
# will be the same
loop_data()


#once list of dodgy transactions created, transactions need to be filtered to make sure they all occur within a month 
# also need to translate into a node graph
def transaction_hashes_to_node_graph(dodgy_transaction_hash_list, transactions_df):
    # filter for start loop
    start_loop = 'start loop'
    # filter to only include transactions which match the transaction hash list 
    loop_transactions = []
    buyers_and_sellers = []
    for transaction_hash in dodgy_transaction_hash_list:
        if transaction_hash != start_loop:
            transaction = transactions_df.loc[transactions_df['transactionhash'] == transaction_hash]
            # print(transaction)
            loop_transactions.append(transaction)
            buyers_and_sellers.append(list(transaction.fromaddress)[0])
            buyers_and_sellers.append(list(transaction.toaddress)[0])    
    buyers_and_sellers = list(dict.fromkeys(buyers_and_sellers))
    return loop_transactions, buyers_and_sellers





# copied and pasted from create node graph v2
def create_json_of_node_data(whale_transactions, intersection, jsn_output_name):    
    whale_transactions = pd.concat(whale_transactions)
    f = open(jsn_output_name, 'w')
    f.write("[\n")
    for sellers_id in intersection:
        name_of_seller = find_wallet_name(sellers_id)
        f.write('{"name":"transactions.' + name_of_seller + '","size":1,"imports":[')
        begin = True
        for index, row in whale_transactions.iterrows():
            if(row.fromaddress == sellers_id):
                name_of_buyer = find_wallet_name(row.toaddress)
                if(begin):
                    f.write('"transactions.' + name_of_buyer + '"')
                    begin = False
                else:
                    f.write(',"transactions.' + name_of_buyer + '"')
        f.write(']},\n')
    f.write("]")

def find_wallet_name(name):
    # return name
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








def create_loops():
    collection_dict = retrieve_all_pickles_into_dict()
    for name, collection in collection_dict.items():
        try:
            if(collection == None):
                return
            transactions_df = collection.transactions_df
            print(name)
            with open('list_of_dodgy_transactions/' + name +
                '.pkl', 'rb') as f:
                bored_ape_list = pickle.load(f)
            whale_transactions, intersection = transaction_hashes_to_node_graph(bored_ape_list, transactions_df)
            create_json_of_node_data(whale_transactions, intersection, 'loop_graph_json/' + name + '_loop_graph.json')
        except:
            print("No data")
            print(name)
# create_loops()