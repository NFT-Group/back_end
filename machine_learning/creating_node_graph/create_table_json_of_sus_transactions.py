import numpy as np
from numpy import genfromtxt
import pandas as pd
from ens import ENS 
from web3 import Web3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pickle
import json
import pathlib
import os
import sys
import inspect
from datetime import datetime

pd.options.mode.chained_assignment = None  # default='warn'
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir1 = os.path.dirname(currentdir)
sys.path.insert(0, parentdir1) 

from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/28b465e090554529bb7913d0504a71bd'))
ns = ENS.fromWeb3(web3)


def transaction_hashes_to_transactions(dodgy_transaction_hash_list, transactions_df, name):
    # filter for start loop
    start_loop = 'start loop'
    loop_id = 0
    # filter to only include transactions which match the transaction hash list 
    transactions_list = []
    buyers_and_sellers = []
    for transaction_hash in dodgy_transaction_hash_list:
        if transaction_hash != start_loop:
            transaction = transactions_df.loc[transactions_df['transactionhash'] == transaction_hash]
            loop_id_name = name.upper() + str(loop_id)
            transaction['loopid'] = loop_id_name
            # have transaction information, now need to add it to the table
            transactions_list.append(transaction)
        else:
            loop_id = loop_id + 1
    return transactions_list

def create_df_of_table_loop_data(transactions_list, name):    
    transactions = pd.concat(transactions_list)
    # sorting by transaction hash
    transactions.sort_values("transactionhash", inplace = True)    
    # dropping duplicate values
    # changing to and from address to the wallet name
    # transactions['toaddress'] = transactions['toaddress'].apply(find_wallet_name)
    # transactions['fromaddress'] = transactions['fromaddress'].apply(find_wallet_name)
    transactions['collection name'] = name
    print(transactions.shape)
    transactions = filter_by_timestamp(transactions, name)
    print(transactions.shape)
    return transactions

def json_table_loops(df_loops):
    df_loops = pd.concat(df_loops)
    df_loops.reset_index(inplace=True)
    cols = df_loops.columns.tolist()
    print(cols)
    df_loops.rename(columns = {'timestamp':'date', 'transactionhash':'transhash'}, inplace = True)
    df_loops = df_loops[['loopid', 'fromaddress', 'toaddress', 'tokenid', 'ethprice', 'date', 'transhash']]
    print(cols) 
    df_loops.sort_values("loopid", inplace = True)
    print(range(len(df_loops)))
    for i in range(len(df_loops)):
        print(i)
        df_loops['fromaddress'][i] = find_wallet_name(df_loops['fromaddress'][i])
        df_loops['toaddress'][i] = find_wallet_name(df_loops['toaddress'][i])
    df_loops.round(2)
    transactions_json = df_loops.to_json('loop_table_json/json_for_table_loops_all_collections.json', orient='records')
    transactions_csv = df_loops.to_csv('loop_table_json/out.csv')
    # print(transactions_json)




def find_wallet_name(name):
    # return name
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

def filter_by_timestamp(datadf, name):
    loop_ids = datadf.loopid.unique()
    num_loops = len(loop_ids)
    num_loops_first_month = 0
    first_transaction = datadf['timestamp'].min()
    first_transaction = datetime.strptime(first_transaction, '%Y-%m-%d')
    for loop_id in loop_ids:
        timestamps = datadf.loc[datadf['loopid'] == loop_id, 'timestamp']
        max_time = max(timestamps)
        min_time = min(timestamps)
        max_time = datetime.strptime(max_time, '%Y-%m-%d')
        min_time = datetime.strptime(min_time, '%Y-%m-%d')
        delta = max_time - min_time
        delta_first_transaction = max_time - first_transaction
        if((delta.days > 7)):
            datadf = datadf[datadf.loopid != loop_id]
        if(delta_first_transaction.days < 30):
            num_loops_first_month += 1
    datadf.sort_values("loopid", inplace = True) 
    print((num_loops_first_month/num_loops) * 100)
    return datadf

def create_loops():
    collection_dict = retrieve_all_pickles_into_dict()
    df_loops = []
    for name, collection in collection_dict.items():
        if(collection == None):
            continue
        transactions_df = collection.transactions_df
        print(name)
        with open('list_of_dodgy_transactions/' + name +
            '.pkl', 'rb') as f:
            bored_ape_list = pickle.load(f)
        transaction_list = transaction_hashes_to_transactions(bored_ape_list, transactions_df, name)
        print("transaction_hashes_to_transactions complete")
        print(len(transaction_list))
        datadf = create_df_of_table_loop_data(transaction_list, name)
        print("create_df_of_table_loop_data complete")
        print(datadf)
        df_loops.append(datadf)
        print(df_loops)
    
    json_table_loops(df_loops)


if __name__ == '__main__':
    create_loops()

