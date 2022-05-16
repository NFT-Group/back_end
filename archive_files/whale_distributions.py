import numpy as np
from numpy import genfromtxt
import pandas as pd
from ordered_set import OrderedSet
import pathlib
from trait_distribution import find_frequency_of_value

def whale_distributions(transactions_data):

    print(transactions_data)
    transactions_data = np.array(transactions_data, dtype=object)

    ''' FIND TOTALS OF OWNERS DISTRIBUTION IN THE WHOLE HISTORY '''

    print(type(transactions_data))
    

    transactions_data = transactions_data[~(transactions_data[:,4] == '0x0000000000000000000000000000000000000000')]
    transactions_data = transactions_data[~(transactions_data[:,-1] == '0')]
    
    # frequency_of_sellers = find_frequency_of_value(transactions_data[:,4])
    # frequency_of_buyers = find_frequency_of_value(transactions_data[:,5])
    # frequency_of_purchases = find_frequency_of_value(transactions_data[:,6])

    # sorted_sellers = {k: v for k, v in sorted(frequency_of_sellers.items(), key = lambda item: item[1])}
    # sorted_buyers = {k: v for k, v in sorted(frequency_of_buyers.items(), key = lambda item: item[1])}
    # sorted_purchases = {k: v for k, v in sorted(frequency_of_purchases.items(), key = lambda item: item[1])}

    ''' END '''

    ''' FIND THE CURRENT DISTRUBUTION OF OWNERS I.E., FINAL TRANSACTIONS
        OF OF EVERY NFT INDEX                                       '''

    unique_id_list = list(OrderedSet(transactions_data[:,6]))
    unique_id_array = np.empty((len(unique_id_list), 3), dtype=object)
    unique_id_array[:,0] = unique_id_list
    transactions_id_list = np.array(transactions_data[:,6], dtype=int)


    for row in range(len(transactions_data)):
        for row2 in range(len(unique_id_array)):
            if(transactions_id_list[row] == int(unique_id_array[row2, 0])):
                unique_id_array[row2, 1] = transactions_data[row, 4]
                unique_id_array[row2, 2] = transactions_data[row, 5]
                break                

    print(unique_id_array)

    frequency_of_sellers = find_frequency_of_value(unique_id_array[:,1])
    frequency_of_buyers = find_frequency_of_value(unique_id_array[:,2])
    frequency_of_purchases = find_frequency_of_value(unique_id_array[:,0])

    sorted_final_sellers = {k: v for k, v in sorted(frequency_of_sellers.items(), key = lambda item: item[1])}
    sorted_final_buyers = {k: v for k, v in sorted(frequency_of_buyers.items(), key = lambda item: item[1])}
    sorted_final_purchases = {k: v for k, v in sorted(frequency_of_purchases.items(), key = lambda item: item[1])}

    ''' INTIIALISE THE FINAL DISTRIBUTION IN THE DICTIONARY FOR BUYERS
        AND SELLERS AND REVERSE ENGINEER THE INITIAL DISTRIBUTION WITH IT'''

    reverse_transaction_data = np.flip(transactions_data, axis=0)
    initial_reverse_buyers = sorted_final_buyers

    list_of_sellers = transactions_data[:,4]
    list_of_buyers = transactions_data[:,5]
    list_of_buyers_and_sellers = np.concatenate([list_of_buyers, list_of_sellers])
    unique_list_of_buyers_and_sellers = OrderedSet(list_of_buyers_and_sellers)
    dict_of_buy_sell = dict.fromkeys(unique_list_of_buyers_and_sellers,0)

    # print(dict_of_buy_sell)

    dict_of_buy_sell_final = dict_of_buy_sell
    dict_of_buy_sell_final.update(initial_reverse_buyers)

    unique_id_list = list(OrderedSet(transactions_data[:,6]))
    transactions_id_list = np.array(transactions_data[:,6], dtype=int)

    for row in range(len(reverse_transaction_data)):
        # seller_current_weight[row] = dict_of_buy_sell[reverse_transaction_data[row, 4]]
        dict_of_buy_sell[reverse_transaction_data[row, 4]] += 1
        dict_of_buy_sell[reverse_transaction_data[row, 5]] -= 1

    # print(dict_of_buy_sell)
    list_of_buy_and_sell_intial = dict_of_buy_sell

    ''' END'''

    ''' INTIALISE STARTING SELLER OWNERSHIP WITH REVERSE ENGINEERED DATA
        AND THEN CREATE ARRAY OF 'CURRENT SELLER WEIGHT', UPDATED
        AFTER EACH TRANSACTION '''

    seller_current_weight = np.zeros([len(transactions_data), 1], dtype=int)
    print(len(transactions_data))
    for row in range(len(transactions_data)):
        seller_current_weight[row] = dict_of_buy_sell[transactions_data[row, 4]]
        dict_of_buy_sell[transactions_data[row, 4]] -= 1
        dict_of_buy_sell[transactions_data[row, 5]] += 1

    print(seller_current_weight)

    return seller_current_weight

    ''' END '''





    
