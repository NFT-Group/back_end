# import ML_models_firestore_trial
import firebase_admin
from firebase_admin import credentials, firestore, db
import pathlib
import json
import pandas as pd
import time
from datetime import date, datetime


apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'
coolCatsAddressArchive = '0x1a92f7381b9f03921564a437210bb9396471050c'
coolCatsAddress = '0x1A92f7381B9F03921564a437210bB9396471050C'
cryptoPunkAddress = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
# cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'
cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'
crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'
pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'

# # get data (all transaction data) from firebase

list_of_names = ["boredape", "boredapekennel", "clonex", "coolcat", "cryptoad", "doodle", "penguin", "punk"]
collection_name_dict = {'boredape': apeAddress, "boredapekennel": boredApeKennelAddress, "clonex": cloneXAddress,
    "coolcat": coolCatsAddress, "cryptoad": crypToadzAddress, "doodle": doodlesAddress,
    "penguin": pudgyPenguinAddress, "punk": cryptoPunkAddress}

cred_pull_transactions_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_transactions_store.json'
cred_pull_transactions = firebase_admin.credentials.Certificate(cred_pull_transactions_key)
transactions_app = firebase_admin.initialize_app(cred_pull_transactions, {
    'databaseURL':'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
    }, name='transactions_app')


def get_transaction_data(address, collection_name, next_collection_name):
    ref = db.reference('/', app=transactions_app)
    # collection_trans = ref.order_by_child('contracthash').equal_to(address).get()
    collection_trans = ref.order_by_child('contracthash').equal_to('0x16205a6048b6af17f1ac1a009bbf2ed9289e6921').get()
    
    return collection_trans
    

def prep_all_collection_data(list_of_names, collection_address_dict):
    list_length = len(list_of_names)
    collection_dict = {}
    for i, name in enumerate(list_of_names):
        address = collection_address_dict[name]
        collection = get_transaction_data(address, name, None)    
        collection_dict.update({name: collection})
    return collection_dict



# randomFromAddress = '0x25e81430a779da09b984dcd09162c1fa0167ca61'
# collection_trans = ref.order_by_child('fromaddress').equal_to(randomFromAddress).get()
# # collection_trans = ref.order_by_child('contracthash').equal_to(coolCatsAddress).get()
# print(collection_trans)    

# # print(prep_all_collection_data(list_of_names, collection_name_dict))

# # cred_pull_transactions_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_transactions_store.json'
# # cred_pull_transactions = firebase_admin.credentials.Certificate(cred_pull_transactions_key)
# # transactions_app = firebase_admin.initialize_app(cred_pull_transactions, {
# #     'databaseURL':'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
# #     }, name='transactions_app')
# weeks_transactions = ref.order_by_child('timestamp').start_at(one_year_ago).get()
# transaction_keys = weeks_transactions.keys()
# total_transaction_counts = [0, 0, 0, 0, 0, 0, 0, 0]
# collection_names = ['Bored Ape Yacht Club', 'CryptoPunks', 'Bored Ape Kennel Club', 'Cool Cats', 'cloneX', 'CrypToadz', 'Doodles', 'Pudgy Penguins']
# for key in transaction_keys:
#     if weeks_transactions[key]['contracthash'] == apeAddress:
#         total_transaction_counts[0] += 1
#     if weeks_transactions[key]['contracthash'] == cryptoPunkAddress:
#         total_transaction_counts[1] += 1
#     if weeks_transactions[key]['contracthash'] == boredApeKennelAddress:
#         total_transaction_counts[2] += 1
#     if weeks_transactions[key]['contracthash'] == coolCatsAddress:
#         total_transaction_counts[3] += 1
#     if weeks_transactions[key]['contracthash'] == cloneXAddress:
#         total_transaction_counts[4] += 1
#     if weeks_transactions[key]['contracthash'] == crypToadzAddress:
#         total_transaction_counts[5] += 1
#     if weeks_transactions[key]['contracthash'] == doodlesAddress:
#         total_transaction_counts[6] += 1
#     if weeks_transactions[key]['contracthash'] == pudgyPenguinAddress:
#         total_transaction_counts[7] += 1

# response_json_array = []

# for i in range(8):
#     response_json_array.append({'name': collection_names[i], 'size': total_transaction_counts[i]})
# # print data required for line chart
# #what data do I need 
# # get data from database (orderbytimestamp)
# #write code and convert to json 
# #axios request to the back end 
# # make function in backend which does relevant 

# average price per day per collection

one_year_ago = time.time() - 15552000 #3.154e7 #number of seconds in a year
one_year_ago = datetime.utcfromtimestamp(int(one_year_ago)).strftime('%Y-%m-%d')
print(one_year_ago)



def add_collection_col_for_mean_price_over_time(dates, collection_df, collection_name):

    # delete first, redundant column
    collection_df = collection_df.iloc[:,0:]

    print("1")
    print(collection_df)

    

    print("2")
    print(collection_df)

    # get the last year's data
    collection_df = collection_df.groupby('timestamp', as_index=False).size()

    print("3")
    print(collection_df)
    
    # change data type to timestamp so we can compare
    collection_df['timestamp'] = pd.to_datetime(collection_df['timestamp'], format='%Y-%m-%d')

    collection_df = collection_df.rename(columns={'size': collection_name})

    print("4")
    print(collection_df)

    dates = dates.merge(collection_df, on='timestamp', how='left')

    print("5")
    print(collection_df)
    
    dates = dates.fillna(method='ffill')
    dates = dates.fillna(0)

    print("6")
    print(collection_df)

    return dates



ref = db.reference('/', app=transactions_app)
dates = pd.DataFrame(pd.date_range(one_year_ago, freq="D", periods=(30*6)))
dates = dates.rename(columns={0: 'timestamp'})

print("here1")
collection_trans = ref.order_by_child('timestamp').start_at(one_year_ago).get()
print("here2")
collection_df = pd.DataFrame.from_dict(collection_trans, orient="index")
collection_df = collection_df[collection_df.fromaddress != '0x0000000000000000000000000000000000000000']
collection_df = collection_df[collection_df.ethprice != 0]

# REMOVE COLUMNS WHICH WON'T BE USED IN PRICE PREDICTION
collection_df = collection_df.drop([
    'tokenid',
    'fromaddress', 
    'toaddress',
    'tokenuri',
    'transactionhash',
    'blocknumber',
], axis=1)

#collection_df = collection_df.drop(collection_df[collection_df.timestamp < one_year_ago].index)

for i, name in enumerate(list_of_names):
    print(name)
    address = collection_name_dict[name]

    collection_df_copy = collection_df
    collection_df_copy = collection_df_copy[collection_df_copy.contracthash == address]
    
    # collection_df.timestamp = pd.to_datetime(collection_df.timestamp)
    # collection_df.timestamp = now - collection_df.timestamp
    # collection_df.timestamp = collection_df.timestamp.apply(lambda x: x.total_seconds())
    dates = add_collection_col_for_mean_price_over_time(dates, collection_df_copy, name)

print(dates)
dates['timestamp'] = dates['timestamp'].dt.strftime("%Y-%m-%d")
dates = dates.astype(str)
print(dates)
dates.to_json(r'multiline.json', orient='records')
# with open("multiline.json", 'w') as outfile:
#     json.dump(dates, outfile)
print(dates)


# transaction_keys = weeks_transactions.keys()

# total_transaction_counts = [0, 0, 0, 0, 0, 0, 0, 0]
# collection_names = ['Bored Ape Yacht Club', 'CryptoPunks', 'Bored Ape Kennel Club', 'Cool Cats', 'cloneX', 'CrypToadz', 'Doodles', 'Pudgy Penguins']
# for key in transaction_keys:
#     if weeks_transactions[key]['contracthash'] == apeAddress:
#         total_transaction_counts[0] += 1
#     if weeks_transactions[key]['contracthash'] == cryptoPunkAddress:
#         total_transaction_counts[1] += 1
#     if weeks_transactions[key]['contracthash'] == boredApeKennelAddress:
#         total_transaction_counts[2] += 1
#     if weeks_transactions[key]['contracthash'] == coolCatsAddress:
#         total_transaction_counts[3] += 1
#     if weeks_transactions[key]['contracthash'] == cloneXAddress:
#         total_transaction_counts[4] += 1
#     if weeks_transactions[key]['contracthash'] == crypToadzAddress:
#         total_transaction_counts[5] += 1
#     if weeks_transactions[key]['contracthash'] == doodlesAddress:
#         total_transaction_counts[6] += 1
#     if weeks_transactions[key]['contracthash'] == pudgyPenguinAddress:
#         total_transaction_counts[7] += 1

# response_json_array = []

# for i in range(8):
#     response_json_array.append({'name': collection_names[i], 'size': total_transaction_counts[i]})

# print((response_json_array))
