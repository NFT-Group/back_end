from web3 import Web3
import contract_details as cd
import time

import numpy as np 
import pandas as pd
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, db

import json

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/1c06ca684f954cfa9c43e80b9112cb8f', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

#red = credentials.Certificate('')
#firebase_admin.initialize_app(cred, { 'databaseURL': "" })

#ref = db.reference('/')

def whale_activity():
    #latest_firebase_block = ref.order_by_child('blocknumber').limit_to_last(1).get()
    #latest_firebase_block = latest_firebase_block[list(latest_firebase_block.keys())[0]]['blocknumber']

    addresses = []
    for line in open("whale_wallets.txt"):
        addresses.append(line[:-2])
    
    block = web3.eth.get_block('latest')
    latest_block_number = block['number']

    

    start_block = latest_block_number - 50000

    print(start_block)

    print(latest_block_number)

    current_block = start_block

    #latest_block_number = 14200000 # remove this

    while current_block <= latest_block_number:
        print(current_block)
        try:
            block = web3.eth.get_block(current_block, full_transactions=True)
        except:
            current_block += 1
            continue #should try again
        #print(block)
        #print(block["number"])
        for i in range(len(block["transactions"])):
            #if i % 10 == 0:
                #print(i)
            txn = block["transactions"][i]
            #from_address = txn["from"]
            from_address = "0x" + txn["input"][2 + (32 * 5):2 + (32 * 5) + 40]
            to_address = "0x" + txn["input"][2 + (32 * 3):2 + (32 * 3) + 40]
            #to_address = txn["to"]
            input = txn["input"]
            if (txn["to"] == cd.openSea and input[0:10] == cd.atomicMatch):
                #from_address = "0x" + txn["input"][2 + (32 * 5):2 + (32 * 5) + 40] #define in terms of 10 + 64*x blocks
                #to_address = "0x" + txn["input"][2 + (32 * 3):2 + (32 * 3) + 40] #also this
                if (from_address in addresses):
                    print("WHALE ACTIVITY SELL")
                    print("from: ", from_address)
                    print("to: ", to_address)
                    print(txn)
                if(to_address in addresses):
                    print("WHALE ACTIVITY BUY")
                    print("from: ", from_address)
                    print("to: ", to_address)
                    print(txn)
        current_block += 1

whale_activity()
