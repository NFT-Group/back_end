import numpy as np
import pandas as pd

def match_trait_dis_values(transactions_data, trait_values_distribution, final_column, unique_header_list):

    # print(unique_data)
    sorted_args = np.argsort(trait_values_distribution[:,0].astype(int))
    trait_values_distribution = trait_values_distribution[sorted_args]

    # id_array = trait_values_distribution[:,0]
    # trait_values_distribution = trait_values_distribution[:,1:]
    # print(id_array)
    # print(trait_values_distribution)
    # number_of_traits = trait_values_distribution.shape[1] - 1
    
    pd_trait_value_dis = pd.DataFrame(transactions_data, columns = 
        ['commonNFTHash', 'hashNumber', 'blockNumber', 'timestamp', 'seller',
        'buyer', 'collectionIndex', 'url', 'priceInETH', 'priceInUSD', 'saleCount',
        'current_seller_weight'])

    # print(unique_header_list)
    unique_header_list.insert(0, 'collectionIndex')
    unique_header_list.append('numberOfTraits')
    pd_transaction_data =  pd.DataFrame(trait_values_distribution)
    pd_transaction_data.columns = unique_header_list

    pd_transaction_data_with_traits = pd_transaction_data.merge(pd_trait_value_dis, on = 'collectionIndex', how = 'inner')

    # concat(transactions_datam, trait_values_distribution, trait_values_distribution[:,0])


    return(pd_transaction_data_with_traits)

    # for i in range(len(trait_values_distribution[:,0])):
    #     for j in range(len(transactions_data[j:,0])):
    #         if(int(trait_values_distribution[i,0]) == int(transactions_data[j,6])):

