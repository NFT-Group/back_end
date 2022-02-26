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
        self.split_data(self.og_token_data)
        self.get_raw_transaction_data(self.og_trans_data)
        self.trait_distribution()
        self.trait_header_list_mod = self.trait_header_list
        self.trait_header_list_mod.insert(0, 'tokenID')
        self.trait_header_list_mod.append('NumOfTraits')
        self.tokens_df = pd.DataFrame(self.trait_values_distribution, columns = self.trait_header_list_mod)
        self.transactions_df = pd.DataFrame(self.transactions_values, columns = self.transactions_keys)
        self.sell_count()

    def split_data(self, og_token_data):
        # initial split of data from an OrderedDict into two lists

        self.id_list = []
        self.metadata_list = []

        for id, meta in self.og_token_data.items():
            id_temp = json.dumps(meta["tokenid"])
            self.id_list.append(id_temp)
            metadata_temp = json.dumps(meta["metadata"])
            metadata_temp = metadata_temp.replace("\\","")[1:-1]
            metadata_temp = json.loads(metadata_temp)
            metadata_temp = json.dumps(metadata_temp["attributes"])
            self.metadata_list.append(metadata_temp)  

        # self.id_list = id_list
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

    def sell_count(self):

            # will append the dataframe with a running count of how many times
            # that particular NFT has sold

            print(self.tokens_df)
            self.count_dict = dict.fromkeys(list(self.tokens_df['tokenID']), 0)

            # count_dict = dict.fromkeys(unique_id, 0)

            self.transactions_id_list = self.transactions_df['tokenid'].tolist()

            # print(self.count_dict)

            for i in range(len(self.transactions_id_list)):
                print(self.transactions_id_list[i])
                if(not (self.transactions_id_list[i] > len(self.id_list))):
                    self.count_dict[str(self.transactions_id_list[i])] += 1

            print(self.count_dict)
            
            # for row in range(count_dict):
            #         for i, j in zip(range(len(transactions_data_id_list)), range(len(sell_count_array))):
            #                 if(unique_id[row] == transactions_data_id_list[i]):
            #                         count_dict[unique_id[row]] += 1
            #                         sell_count_array[i,0] = count_dict[unique_id[row]]
          
        
    def trait_distribution(self):
        # determine distribution of traits from a file input, outputs a list of 
        # unique header values (e.g. 'earing', 'fur colour' etc. ) and an numpy array
        # of what percentage of times feature appears in collection 
        # # print(self.id_list[0])
        # print(self.metadata_list)
        # print(type(self.metadata_list))
        # exit()
        self.id_list_np = np.array(self.id_list).reshape([len(self.id_list), 1])
        traitList = []

        # print(self.metadata_list.shape)


        # print(self.metadata_list)
        # print(type(self.metadata_list))
        # exit()

        # converting json formatted description of each NFTs traits into python
        # list format
        for i in range(len(self.id_list_np)):
            traitList.append(re.findall('"([^"]*)"', self.metadata_list[i]))

        # print(traitList)
        # exit()

        # json data is in format "Trait": TraitHeader : "Value" : value, we are only
        # interested in the trait header and the value of the header 
        # use trait list to create a full list of every header (this is repeated in 
        # position 1)
        trait_header_list = []
        for i in range(len(traitList)):
            for j in range(len(traitList[i])):
                if ((j % 4) == 1):
                    trait_header_list.append(traitList[i][j])

        # print(trait_header_list)
        # exit()
        
        # make the header list unique (using orderedlist to stop non-determinism)
        my_temp_set = OrderedSet(trait_header_list)
        unique_header_list = list(my_temp_set)
        print(unique_header_list)

        # create trait values which will create a numpy array of all the trait values
        # for the correct header e.g. 'gold hoop' within 'earing' header
        print(len(traitList))
        print(len(unique_header_list))
        trait_values_np = np.empty([len(traitList) ,len(unique_header_list)], dtype=object)
        # print(trait_values_np.shape)
        # print(len(traitList))
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
