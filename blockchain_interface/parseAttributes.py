import numpy as np 
import pandas as pd
from datetime import datetime
import json

import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate('allTokens_key.json')
firebase_admin.initialize_app(cred, 
{
'databaseURL': "https://alltokens-8ff48-default-rtdb.europe-west1.firebasedatabase.app/"
})

def save_to_firebase_new(hash, dfjson):
    ref = db.reference('/')
    ref.child(hash).set(dfjson)


def convert_historical_CSV(CSVpre):
    data = []
    for line in open(CSVpre):
        temp = line.strip().split("|")
        data.append(temp)

    data_npy = np.array(data)
    for i in range(len(data_npy)):
        data_npy[i,3] = datetime.utcfromtimestamp(int(data_npy[i,3])).strftime('%Y-%m-%d')

    DF = pd.DataFrame(data_npy[:, :-1])
    DF.columns = ['contracthash', 'transactionhash', 'blocknumber', 'timestamp', 'fromaddress', 'toaddress', 'tokenid', 'tokenuri', 'ethprice']
    DF['blocknumber'] = DF['blocknumber'].astype(int)
    DF['tokenid'] = DF['tokenid'].astype(int)
    DF['ethprice'] = DF['ethprice'].astype(float)
    dfjson = DF.to_json(orient='records')
    parsed = json.loads(dfjson)
    return parsed

def convert_alltokens_CSV(CSVpre):
    
    data = []
    for line in open(CSVpre):
        temp = line.strip().split("|")
        data.append(temp[:])

    data_npy = np.array(data)
    #for i in range(len(data_npy)):
        #data_npy[i,3] = datetime.utcfromtimestamp(int(data_npy[i,3])).strftime('%Y-%m-%d')

    DF = pd.DataFrame(data_npy[:, :])
    DF.columns = ['tokenid', 'metadata']
    DF['tokenid'] = DF['tokenid'].astype(int)
    dfjson = DF.to_json(orient='records')
    parsed = json.loads(dfjson)
    return parsed

"""
def upload_to_database_useful(df):
    cred = credentials.Certificate('key4.json')
    firebase_admin.initialize_app(cred, 
    {
    'databaseURL': 'https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    db = firestore.client()
    doc_ref = db.collection(u'historicaldata2')
    # Import data
    tmp = df.to_dict(orient='records')
    list(map(lambda x: doc_ref.add(x), tmp))
"""
#update_field()

#create_fields_for_demonstration()

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x1a92f7381b9f03921564a437210bb9396471050c.csv")
#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6.csv")
#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e.csv")
#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B.csv")

# still to do 

#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB.csv")
#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623.csv")
#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D.csv")
#convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xBd3531dA5CF5857e7CfAA92426877b022e612cf8.csv")


#tdf = convert_historical_CSV("../getting-some-sweet-juicy-data/past_0xBd3531dA5CF5857e7CfAA92426877b022e612cf8.csv")
# tdf2 = convert_historical_CSV("../getting-some-sweet-juicy-data/past_0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623.csv")
# tdf3 = convert_historical_CSV("../getting-some-sweet-juicy-data/past_0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D.csv")
# tdf4 = convert_historical_CSV("../getting-some-sweet-juicy-data/past_0xBd3531dA5CF5857e7CfAA92426877b022e612cf8.csv")


"""
print(json.dumps(tdf[0], indent=4))
print(json.dumps(tdf[2], indent=4))
print(tdf[2]["transactionhash"])
"""

print(len(tdf))

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x1a92f7381b9f03921564a437210bb9396471050c.csv")
print("COOLCATS")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "coolcat" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])
    #print(name + " " + str(tdf[i]))

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6.csv")
print("CRYPTOADZ")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "cryptoad" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e.csv")
print("DOODLES")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "doodle" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B.csv")
print("CLONEX")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "clonex" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB.csv")
print("CRYPTOPUNKS")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "punk" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623.csv")
print("BOREDAPEKENNEL")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "boredapekennel" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D.csv")
print("BOREDAPE")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "boredape" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

################

tdf = convert_alltokens_CSV("../getting-some-sweet-juicy-data/all_0xBd3531dA5CF5857e7CfAA92426877b022e612cf8.csv")
print("PUDGYPENGUINS")

for i in range(len(tdf)):
    if (i % 100 == 0):
        print(i)
    name = "penguin" + str(tdf[i]["tokenid"])
    save_to_firebase_new(name, tdf[i])

#save_to_firebase_new(tdf)


#upload_to_database_useful(tdf1)


# upload_to_database_useful(tdf2)
# upload_to_database_useful(tdf3)
# upload_to_database_useful(tdf4)
