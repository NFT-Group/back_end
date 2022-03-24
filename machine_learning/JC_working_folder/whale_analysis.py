import pandas as pd

transactions_df = pd.read_pickle("transactions_df.pkl")
whale_list_df = pd.read_csv("whale_list_supreme.csv", names=["whale_list"], header = None)

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