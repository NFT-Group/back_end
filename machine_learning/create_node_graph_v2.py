import numpy as np
from numpy import genfromtxt
import pandas as pd
# from ens import ENS 
# from web3 import Web3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# from trait_distribution import trait_distribution 
import json
import pathlib
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir1 = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir1)
sys.path.insert(0, parentdir2) 

from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict


def create_node_graph_data(transactions_df, jsn_output_name):
    transactions_df.sort_values("running_whale_weight", ascending = False, inplace = True)
    top_transactions = transactions_df['fromaddress'].unique()
    top_transactions = top_transactions[0:200]
    buyers_from_top_seller_list = []
    for seller_id in top_transactions:
        temp_buyers = transactions_df.loc[transactions_df['fromaddress'] == seller_id, 'toaddress']
        buyers_from_top_seller_list.append(temp_buyers.tolist())
    # go from a list of lists, to just list of strings
    buyers_from_top_seller_list = [address for sublist in buyers_from_top_seller_list for address in sublist]


    # at this point have a list of all buyers who have bought from the top sellers
    # get the intersection of the buyers and the sellers
    intersection_buyers = np.intersect1d(top_transactions, buyers_from_top_seller_list)
    print(intersection_buyers.shape)
    whale_transactions = []
    

    seller_from_top_seller_list = []
    for buyer_id in top_transactions:
        temp_seller = transactions_df.loc[transactions_df['toaddress'] == buyer_id, 'fromaddress']
        seller_from_top_seller_list.append(temp_seller.tolist())
    # go from a list of lists, to just list of strings
    seller_from_top_seller_list = [address for sublist in seller_from_top_seller_list for address in sublist]

    # sellers from top seller list is all people who have sold to top 200 sellers
    # get the intersection of these sellers and the top 200 sellers
    intersection_sellers = np.intersect1d(top_transactions, seller_from_top_seller_list)
    print(intersection_sellers.shape)

    intersection = np.union1d(intersection_buyers, intersection_sellers)

    print(intersection.shape)
    # 
    for line_number, (index, row) in enumerate(transactions_df.iterrows()):
        if ((row.fromaddress in intersection) and (row.toaddress in intersection)):
            whale_transactions.append(transactions_df.iloc[[line_number]])
    
    whale_transactions = pd.concat(whale_transactions)
    whale_transactions.to_csv('shows.csv')
    f = open(jsn_output_name, 'w')
    f.write("[\n")
    for sellers_id in intersection:
        # name_of_seller = find_wallet_name(sellers_id)
        f.write('{"name":"transactions.' + sellers_id + '","size":1,"imports":[')
        begin = True
        for index, row in whale_transactions.iterrows():
            if(row.fromaddress == sellers_id):
                name_of_buyer = row.toaddress
                if(begin):
                    f.write('"transactions.' + name_of_buyer + '"')
                    begin = False
                else:
                    f.write(',"transactions.' + name_of_buyer + '"')
        f.write(']},\n')
    f.write("]")

def node_data():
    collection_dict = retrieve_all_pickles_into_dict()
    for name, collection in collection_dict.items():
        if(collection != None):
            transactions_df = collection.transactions_df
            print(name)
            # print(transactions_df)
            create_node_graph_data(transactions_df, 'node_graph_json/' + name + '_node_graph.json')
node_data()