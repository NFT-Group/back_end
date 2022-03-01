import numpy as np
from trait_distribution import trait_distribution 
import json
from collections import OrderedDict 
from ordered_set import OrderedSet
import pandas as pd
import re
from trait_distribution import find_frequency_of_value

class Collection:

    def __init__(self, og_token_data, og_trans_data):
        self.og_token_data = og_token_data
        self.og_trans_data = og_trans_data

    def prep_data(self):
        # read in data from firebase into manageable formats
        self.split_data(self.og_token_data)
        self.get_raw_transaction_data(self.og_trans_data)
        # determine trait distribution
        self.trait_distribution()
        self.trait_header_list_mod = self.trait_header_list
        self.trait_header_list_mod.insert(0, 'tokenID')
        self.trait_header_list_mod.append('NumOfTraits')
        self.tokens_df = pd.DataFrame(self.trait_values_distribution, columns = self.trait_header_list_mod)
        self.transactions_df = pd.DataFrame(self.transactions_values, columns = self.transactions_keys)
        self.add_sell_count()
        self.add_whale_distribution()

        print(self.transactions_df)

        # self.transactions_df.to_pickle("transactions_df.pkl")
        # self.tokens_df.to_pickle("tokens_df.pkl")


    def split_data(self, og_token_data):
        # initial split of data from an OrderedDict into two lists

        self.token_id_list = []
        self.metadata_list = []

        for id, meta in self.og_token_data.items():
            id_temp = json.dumps(meta["tokenid"])
            self.token_id_list.append(id_temp)
            metadata_temp = json.dumps(meta["metadata"])
            metadata_temp = metadata_temp.replace("\\","")[1:-1]
            metadata_temp = json.loads(metadata_temp)
            metadata_temp = json.dumps(metadata_temp["attributes"])
            self.metadata_list.append(metadata_temp)  

        # self.token_id_list = token_id_list
        # self.metadata_list = metadata_list

    def get_raw_transaction_data(self, og_trans_data):
        # initial split of transactions data from ordered dict into a 
        # list of headers and a list of all the raw data without headers

        data_list = []

        for id, other_data in self.og_trans_data.items():
            transaction_hash = json.dumps(id)
            data_temp = json.loads(json.dumps(other_data))
            data_list.append(data_temp)
            transactions_keys = list(data_list[0].keys())
            transactions_values = [list(d.values()) for d in data_list]
        
        self.transactions_keys = transactions_keys
        self.transactions_values = transactions_values

    def add_sell_count(self):

            # will append the dataframe with a running count of how many times
            # that particular NFT has sold

            self.count_dict = dict.fromkeys(list(self.tokens_df['tokenID']), 0)

            # count_dict = dict.fromkeys(unique_id, 0)

            self.transactions_id_list = self.transactions_df['tokenid'].tolist()

            self.sell_count_array = np.zeros([len(self.transactions_id_list), 1])
            for i in range(len(self.transactions_id_list)):
                if(self.transactions_id_list[i] <= len(self.token_id_list)):
                    try:
                        self.count_dict[str(self.transactions_id_list[i])] += 1
                        self.sell_count_array[i, 0] = self.count_dict[str(self.transactions_id_list[i])]
                    except KeyError:
                        continue

            self.transactions_df = self.transactions_df.assign(
                running_sell_count = self.sell_count_array.tolist())        
        
    def trait_distribution(self):
        # determine distribution of traits from a file input, outputs a list of 
        # unique header values (e.g. 'earing', 'fur colour' etc. ) and an numpy array
        # of what percentage of times feature appears in collection 
        self.id_list_np = np.array(self.token_id_list).reshape([len(self.token_id_list), 1])
        traitList = []

        # converting json formatted description of each NFTs traits into python
        # list format
        for i in range(len(self.id_list_np)):
            traitList.append(re.findall('"([^"]*)"', self.metadata_list[i]))

        # json data is in format "Trait": TraitHeader : "Value" : value, we are only
        # interested in the trait header and the value of the header 
        # use trait list to create a full list of every header (this is repeated in 
        # position 1)
        trait_header_list = []
        for i in range(len(traitList)):
            for j in range(len(traitList[i])):
                if ((j % 4) == 1):
                    trait_header_list.append(traitList[i][j])
        
        # make the header list unique (using orderedlist to stop non-determinism)
        my_temp_set = OrderedSet(trait_header_list)
        unique_header_list = list(my_temp_set)

        # create trait values which will create a numpy array of all the trait values
        # for the correct header e.g. 'gold hoop' within 'earing' header
        trait_values_np = np.empty([len(traitList) ,len(unique_header_list)], dtype=object)
        for i in range(len(traitList)):
            for j in range(len(traitList[i])):
                if ((j % 4) == 1): 
                    for k in range(len(unique_header_list)):
                        if(unique_header_list[k] == traitList[i][j]):
                            trait_values_np[i,k] = str(traitList[i][j+2])
                            
        # get counts of how many traits each nft has
        number_of_traits = np.zeros([len(trait_values_np),1])
        for i in range(len(trait_values_np)):
            number_of_traits[i,0] = len(unique_header_list) - np.count_nonzero(trait_values_np[i,:] == None)

        # return a dictionary of the distributions of each quantity of traits
        number_of_traits = number_of_traits.astype(str)
        frequency_of_traits = find_frequency_of_value(number_of_traits[:,0])

        # create array of each NFT's trait count 
        trait_frequency_per_nft = np.zeros([len(trait_values_np),1])
        for i in range(len(trait_frequency_per_nft)):
            trait_frequency_per_nft[i,0] = frequency_of_traits[number_of_traits[i,0]] 

        # create array of empty dictionaries
        frequency_dic = [dict() for x in range(len(unique_header_list))]
        # fill dictionaries with frequency of header values 
        for i in range(len(unique_header_list)):
            frequency_dic[i] = find_frequency_of_value(trait_values_np[:,i])

        # create array which contains the count of how many times a trait appears
        trait_values_count_np = np.empty([len(traitList), len(unique_header_list)])
        for i in range(len(trait_values_np)):
            for j in range(len(unique_header_list)):
                trait_values_count_np[i][j] = frequency_dic[j][trait_values_np[i][j]]

        # sandwiches the list of trait distributions with the NFT IDs in column[0] 
        # and the number of traits in the final column
        trait_values_count_np = np.column_stack((self.id_list_np[:,0], trait_values_count_np))
        trait_values_count_np = np.column_stack((trait_values_count_np, trait_frequency_per_nft))
        # print(trait_values_count_np)

        # change count to % so we normalise the data for varying collection sizes
        trait_values_count_np[:,1:] = trait_values_count_np[:,1:].astype(float)/len(trait_values_count_np)
        trait_values_distribution = trait_values_count_np
        # print(trait_values_distribution
        # print(trait_values_distribution)

        self.trait_header_list = unique_header_list
        self.trait_values_distribution = trait_values_distribution

    def add_whale_distribution(self):

        ''' FIND THE CURRENT DISTRUBUTION OF OWNERS I.E., FINAL TRANSACTIONS
        OF OF EVERY NFT INDEX '''

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
            running_whale_weight = self.sell_count_array.tolist())     
