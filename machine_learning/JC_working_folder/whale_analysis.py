import pandas as pd


def whale_percentage_transactions(transactions_df, whale_list_df):
    

    # get list of sellers and buyers 
    sellers_df = transactions_df[['fromaddress']]
    buyers_df = transactions_df[['toaddress']]
    buyers_df = buyers_df.rename(columns ={'toaddress':'fromaddress'})

    # combine sellers and buyers and make unique e.g., so have one list of all sellers and buyers
    buyers_sellers = sellers_df.append(buyers_df, ignore_index = True)
    buyers_sellers = buyers_sellers.fromaddress.unique()

    # find the transactions where the whales are sellers  
    whale_transactions_sellers = transactions_df.merge(
                whale_list_df,
                left_on='fromaddress', 
                right_on='whale_list', 
                how='inner')

    #  find the transactions where the whales are buyers  
    whale_transactions_buyers = transactions_df.merge(
                whale_list_df,
                left_on='toaddress', 
                right_on='whale_list', 
                how='inner')

    # stop double counting by finding the number of transactions that have whale buyers and whale sellers
    whale_transactions_joined = whale_transactions_buyers.merge(
                whale_transactions_sellers,
                left_on='transactionhash', 
                right_on='transactionhash', 
                how='inner')

    total_whale_trans = len(whale_transactions_buyers) + len(whale_transactions_sellers) - len(whale_transactions_joined)

    print("Total number of buyers and sellers is ", len(buyers_sellers))
    print("Total whale count is ", len(whale_list_df))

    print("Whale percentage of transactions is: ", (total_whale_trans)/len(transactions_df))

    print("Whale percentage of buyers/sellers is: ", len(whale_list_df)/len(buyers_sellers))

def find_all_loops(list_of_whales):
    dodgy_transactions_list = []
    for whale_address in list_of_whales:
        list_of_addresses_in_loop = []
        list_of_addresses_in_loop.append(whale_address)
        find_all_buyers(whale_address, whale_address, list_of_addresses_in_loop, 0)
        if(len(list_of_addresses_in_loop) != 1):
            # temp_df = pd.DataFrame(list_of_addresses_in_loop, columns = [whale_address])
            dodgy_transactions_list.insert(0, whale_address)
            dodgy_transactions_list.append(list_of_addresses_in_loop)
            print(len(dodgy_transactions_list))
            # print(list_of_addresses_in_loop)
    data_transposed = zip(dodgy_transactions_list)
    df = pd.DataFrame(data_transposed)
    print(df)
    return df



# find all buyers of a seller, if a buyer is a target address return true and 
# add seller address and whale address to the list of addresses 
def find_all_buyers(whale_address, target_address, list_of_addresses_in_loop, count):
    # list_of_addresses_in_loop.append('another_one')
    count = count + 1
    if(count > 2):
        return False
    list_of_buyers = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'toaddress'])
    list_of_transactions = (transactions_df.loc[transactions_df['fromaddress'] == whale_address, 'transactionhash']).tolist()
    list_of_buyers = list_of_buyers.tolist()
    found = False
    if(len(list_of_buyers) == 0):
        return False
    for i in range(len(list_of_buyers)):
        if (list_of_buyers[i] == target_address):
            list_of_addresses_in_loop.append("Another one")
            list_of_addresses_in_loop.append(whale_address)
            list_of_addresses_in_loop.append(list_of_transactions[i])
            found = True
        if(find_all_buyers(list_of_buyers[i], target_address, list_of_addresses_in_loop, count)):
            list_of_addresses_in_loop.append(whale_address)
            list_of_addresses_in_loop.append(list_of_transactions[i])
            found = True
    if(found):
        return True
    return False


transactions_df = pd.read_pickle("transactions_df.pkl")
whale_list_df = pd.read_csv("whale_list_supreme.csv", names=["whale_list"], header = None)
df = pd.DataFrame((find_all_loops(whale_list_df.whale_list.tolist())))
# print(df)
df.to_csv('list_of_looping_transactions.csv', index = False)
# print(df)
# find_all_buyers('0x5a418d8bc0c074a4a8fa88d1322dc51cc1cb9d29', '0x5a418d8bc0c074a4a8fa88d1322dc51cc1cb9d29', address_list, 0)
# print(address_list)