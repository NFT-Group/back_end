from web3 import Web3
import contract_details as cd
import time

import numpy as np 
import pandas as pd
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, db


import json

cred = credentials.Certificate('allCollections_key.json')
firebase_admin.initialize_app(cred, { 'databaseURL': "https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/" })

ref = db.reference('/')


latest_firebase_block = ref.order_by_child('blocknumber').get()
#print(latest_firebase_block)
key_list = list(latest_firebase_block.keys())
for key in key_list:
    if latest_firebase_block[key]["contracthash"] == cd.cloneXAddress:
        timestamp = latest_firebase_block[key]["timestamp"]
        if str(timestamp)[0] == '1':
            print(timestamp)

"""
new_ref = db.reference('/' + key)
errant_block = new_ref.get()
#print(errant_block)
#print(errant_block["timestamp"])
errant_block["timestamp"] = datetime.utcfromtimestamp(int(errant_block['timestamp'])).strftime('%Y-%m-%d')
print(errant_block)
ref.child(key).set(errant_block)


new_entry = ref.order_by_value().equal_to('0x5747f908aaf41555f3ddc5679b8c4cca889fb9e87d90151ea1893fcabb609ef6').get()
print("new entry is")
print(new_entry)
"""

#for i in list(latest_firebase_block.keys()):
    #if latest_firebase_block[i]
    #print(len(list(latest_firebase_block.keys())))