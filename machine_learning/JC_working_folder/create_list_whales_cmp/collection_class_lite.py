import numpy as np
import json
from collections import OrderedDict 
from ordered_set import OrderedSet
import pandas as pd
import re
from trait_distribution import find_frequency_of_value

class Collection_lite:

    def __init__(self, og_trans_data):
        self.og_trans_data = og_trans_data

    def prep_data(self):
        self.get_raw_transaction_data(self.og_trans_data)
        # print(self.og_trans_data)
        self.transactions_df = pd.DataFrame(self.transactions_values, columns = self.transactions_keys)
        
        self.add_whale_distribution()

    def get_raw_transaction_data(self, og_trans_data):
        # initial split of transactions data from ordered dict into a 
        # list of headers and a list of all the raw data without headers

        data_list = []
        self.transactions_keys = []
        self.transactions_values = []


        for id, other_data in self.og_trans_data.items():
            transaction_hash = json.dumps(id)
            data_temp = json.loads(json.dumps(other_data))
            data_list.append(data_temp)
            self.transactions_keys = list(data_list[0].keys())
            self.transactions_values = [list(d.values()) for d in data_list]
        

        
    
    def add_whale_distribution(self):

        ''' FIND THE CURRENT DISTRUBUTION OF OWNERS I.E., FINAL TRANSACTIONS
        OF OF EVERY NFT INDEX '''
        # print(self.transactions_df)
        final_owners_list = self.transactions_df['tokenid'].unique()
        unique_id_array = np.empty((len(final_owners_list), 3), dtype=object)
        unique_id_array[:,0] = final_owners_list
        transactions_id_list = np.array(self.transactions_df['tokenid'], dtype=int)

        for row in range(self.transactions_df.shape[0]):
            for row2 in range(len(unique_id_array)):
                if(transactions_id_list[row] == int(unique_id_array[row2, 0])):
                    unique_id_array[row2, 1] = self.transactions_df.loc[self.transactions_df.index[row], 'fromaddress']
                    unique_id_array[row2, 2] = self.transactions_df.loc[self.transactions_df.index[row], 'toaddress']
                    break


        frequency_of_sellers = find_frequency_of_value(unique_id_array[:,1])
        frequency_of_buyers = find_frequency_of_value(unique_id_array[:,2])
        frequency_of_purchases = find_frequency_of_value(unique_id_array[:,0])

        sorted_final_sellers = {k: v for k, v in sorted(frequency_of_sellers.items(), key = lambda item: item[1])}
        sorted_final_buyers = {k: v for k, v in sorted(frequency_of_buyers.items(), key = lambda item: item[1])}
        sorted_final_purchases = {k: v for k, v in sorted(frequency_of_purchases.items(), key = lambda item: item[1])}

        ''' INTIIALISE THE FINAL DISTRIBUTION IN THE DICTIONARY FOR BUYERS
        AND SELLERS AND REVERSE ENGINEER THE INITIAL DISTRIBUTION WITH IT'''

        reverse_transaction_data = self.transactions_df.iloc[::-1]
        initial_reverse_buyers = sorted_final_buyers

        list_of_sellers = self.transactions_df['fromaddress']
        list_of_buyers = self.transactions_df['toaddress']
        list_of_buyers_and_sellers = list_of_buyers + list_of_sellers
        unique_list_of_buyers_and_sellers = OrderedSet(list_of_buyers_and_sellers)
        dict_of_buy_sell = dict.fromkeys(unique_list_of_buyers_and_sellers,0)

        dict_of_buy_sell_final = dict_of_buy_sell
        dict_of_buy_sell_final.update(initial_reverse_buyers)

        for row in range(len(reverse_transaction_data)):
            try:
                dict_of_buy_sell[reverse_transaction_data.loc[self.transactions_df.index[row], 'fromaddress']] += 1
                dict_of_buy_sell[reverse_transaction_data.loc[self.transactions_df.index[row], 'toaddress']] -= 1
            except KeyError:
                continue

        ''' INTIALISE STARTING SELLER OWNERSHIP WITH REVERSE ENGINEERED DATA
        AND THEN CREATE ARRAY OF 'CURRENT SELLER WEIGHT', UPDATED
        AFTER EACH TRANSACTION '''

        seller_current_weight = np.zeros([self.transactions_df.shape[0], 1], dtype=int)

        for row in range(self.transactions_df.shape[0]):
            try:
                seller_current_weight[row] = dict_of_buy_sell[
                    self.transactions_df.loc[
                        self.transactions_df.index[row], 'fromaddress']]
                dict_of_buy_sell[self.transactions_df.loc[
                    self.transactions_df.index[row], 'fromaddress']] -= 1
                dict_of_buy_sell[self.transactions_df.loc[
                    self.transactions_df.index[row], 'toaddress']] += 1
            except KeyError:
                continue

        self.transactions_df = self.transactions_df.assign(
            running_whale_weight = seller_current_weight.tolist())     
