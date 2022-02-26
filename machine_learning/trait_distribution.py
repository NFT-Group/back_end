import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
import re
import sys
import json
import requests
from ordered_set import OrderedSet

# pass in a column and return a dictionary of how frequently trait occurs 
# within column 
def find_frequency_of_value(column):
    # print(type(column))
    classes_set = OrderedSet(column)
    classes = np.array(list(classes_set))
    freq_labels = dict.fromkeys(classes, 0)
    for label in column:
        freq_labels[label] += 1

    return(freq_labels)

# determine distribution of traits from a file input, outputs a list of 
# unique header values (e.g. 'earing', 'fur colour' etc. ) and an numpy array
# of what percentage of times feature appears in collection 
def trait_distribution(unique_data, unique_json):
    
    # print("UNIQUE DATA", unique_json[0])
    # exit()
    unique_data = np.array(unique_data).reshape([len(unique_data), 1])
    traitList = []

    # converting json formatted description of each NFTs traits into python
    # list format
    print(unique_json)
    print(type(unique_json))
    exit()
    for i in range(len(unique_json)):
        traitList.append(re.findall('"([^"]*)"', unique_json[i]))

    # print("TRAIT LIST", traitList)

    # json data is in format "Trait": TraitHeader : "Value" : value, we are only
    # interested in the trait header and the value of the header 
    # use trait list to create a full list of every header (this is repeated in 
    # position 1)
    trait_header_list = []
    for i in range(len(traitList)):
        for j in range(len(traitList[i])):
            if ((j % 4) == 1):
                trait_header_list.append(traitList[i][j])

    #print(trait_header_list)
    
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
    trait_values_count_np = np.column_stack((unique_data[:,0], trait_values_count_np))
    trait_values_count_np = np.column_stack((trait_values_count_np, trait_frequency_per_nft))
    # print(trait_values_count_np)

    # change count to % so we normalise the data for varying collection sizes
    trait_values_count_np[:,1:] = trait_values_count_np[:,1:].astype(float)/len(trait_values_count_np)
    trait_values_distribution = trait_values_count_np
    # print(trait_values_distribution

    return(unique_header_list, trait_values_distribution)

