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




def find_all_loops(list_of_whales, transactions_df):
    dodgy_transactions_list = []
    for whale_address in list_of_whales:
        list_of_addresses_in_loop = []
        find_all_buyers(transactions_df, whale_address, whale_address, list_of_addresses_in_loop, 0)
        if(len(list_of_addresses_in_loop) != 0):
            dodgy_transactions_list.append(list_of_addresses_in_loop)
            print(len(dodgy_transactions_list))

    flat_list = [item for sublist in dodgy_transactions_list for item in sublist]
    return flat_list



# find all buyers of a seller, if a buyer is a target address return true and 
# add seller address and whale address to the list of addresses 
def find_all_buyers(transactions_df, whale_address, target_address, list_of_addresses_in_loop, count):
    count = count + 1
    if(count > 3):
        return False
    list_of_buyers = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'toaddress'])
    list_of_transactions = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'transactionhash']).tolist()
    list_of_buyers = list_of_buyers.tolist()
    found = False
    if(len(list_of_buyers) == 0):
        return False
    for i in range(len(list_of_buyers)):
        if (list_of_buyers[i] == target_address):
            list_of_addresses_in_loop.append("start loop")
            list_of_addresses_in_loop.append(list_of_transactions[i])
            return True
        elif(find_all_buyers(transactions_df, list_of_buyers[i], target_address, list_of_addresses_in_loop, count)):
            list_of_addresses_in_loop.append(list_of_transactions[i])
            found = True
    if(found):
        return True
    return False




def loop_data():
    collection_dict = retrieve_all_pickles_into_dict()
    for name, collection in collection_dict.items():
            transactions_df = collection.transactions_df
            print(name)
            transactions_df.sort_values("running_whale_weight", ascending = False, inplace = True)
            top_whale_sellers = transactions_df['fromaddress'].unique()
            top_whale_sellers = top_whale_sellers[0:100]
            flat_list = find_all_loops(top_whale_sellers, transactions_df)
            with open('list_of_dodgy_transactions/' + name +
                '.pkl', 'wb') as handle:
                    pickle.dump(flat_list, handle)
                    print("Created")
            print(flat_list)


# This will rerun all of the loop data - creating a list of transaction hashes of dodgy transactions (loops), 
# where the "to address" in the first transaction after 'start loop' and the 'from address' in the last transaction hash
# will be the same
# loop_data()

with open('list_of_dodgy_transactions/boredape.pkl', 'rb') as f:
    bored_ape_list = pickle.load(f)
    print(bored_ape_list)
