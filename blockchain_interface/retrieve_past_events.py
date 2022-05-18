# this was used as one-time code to populate the firebase with data

from web3 import Web3
import contract_details as cd
import time
import numpy as np
import pandas as pd
import json
from datetime import datetime

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/988b74d457e5454eb83301c82292c960', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate('allCollections_key.json')
firebase_admin.initialize_app(cred, { 'databaseURL': "https://allcollections-6e66c-default-rtdb.europe-west1.firebasedatabase.app/" })

ref = db.reference('/')

#web3 = websockets.client.WebSocketClientProtocol('wss://mainnet.infura.io/ws/v3/bba210d6663b4c0999d9ccb2c34a91bd', max_size=1000000)

def retrieve(contract_abi, contract_address, start, end, step):
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    for i in range(start, (end - step) + 1, step):
        filter = contract.events.Transfer.createFilter(fromBlock=i, toBlock=(i + step - 1))
        events = filter.get_all_entries()
        if len(events) == 0:
            print("blocks" + str(i) + " to " + str(i + step) + " are empty of this contract")
            continue
        transaction_hash = ""
        for i in range(len(events)):
            #print(events[i])
            previous_transaction_hash = transaction_hash
            transaction_hash = (events[i]["transactionHash"]).hex()
            if transaction_hash == previous_transaction_hash:
                continue
            transaction = web3.eth.get_transaction(transaction_hash)
            input = (transaction["input"])
            if input[0:10] == cd.atomicMatch or input[0:10] == cd.buyPunk or transaction["to"] == cd.openSea:
                #print(event)
                #print(transaction)
                block_hash = (transaction["blockHash"]).hex()
                block = web3.eth.getBlock(block_hash)
                block_number = (transaction["blockNumber"])
                timestamp = block["timestamp"]
                wei_value = transaction["value"]
                ether_value = Web3.fromWei(wei_value, 'ether')
                from_address = "0x" + transaction["input"][2 + (32 * 5):2 + (32 * 5) + 40] #define in terms of 10 + 64*x blocks
                to_address = "0x" + transaction["input"][2 + (32 * 3):2 + (32 * 3) + 40] #also this
                tokenID = transaction["input"][10 + (64 * 62):10 + (64 * 62) + 8]
                tokenID = int(tokenID, 16)
                try:
                    tokenURI = contract.functions.tokenURI(tokenID).call()
                except:
                    tokenURI = "missing_token"
                data = ""
                data += contract_address + "|" + transaction_hash + "|" + str(block_number) + "|" + str(timestamp) + "|"
                data += from_address + "|" + to_address + "|" + str(tokenID) + "|" + str(tokenURI) + "|" + str(ether_value) + "|" + "-"
                data += "\n"
                print(block_number)

def convert_list_to_transaction_json(data):
    data_npy = np.array(data)
    DF = pd.DataFrame(data_npy).T
    
    DF.columns = ['contracthash', 'transactionhash', 'blocknumber', 'timestamp', 'fromaddress', 'toaddress', 'tokenid', 'tokenuri', 'ethprice']
    DF['timestamp'] = datetime.utcfromtimestamp(int(DF['timestamp'])).strftime('%Y-%m-%d')
    DF['blocknumber'] = DF['blocknumber'].astype(int)
    DF['tokenid'] = DF['tokenid'].astype(int) #crashed with cryptopunk! solved!
    DF['ethprice'] = DF['ethprice'].astype(float)
    dfjson = DF.to_json(orient='records')
    parsed = json.loads(dfjson)

    print(parsed)
    return parsed

def save_to_firebase_new(txnhash, dfjson):
    #ref = db.reference('/')
    #print("hash")
    #print(txnhash)
    #print("json")
    #print(dfjson[0])
    print(txnhash)
    ref.child(txnhash).set(dfjson[0])

def retrieve_punks(start, end, step):
    contract_abi = cd.cryptoPunkABI
    contract_address = cd.cryptoPunkAddress
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    for i in range(start, (end - step) + 1, step):
        filter = contract.events.Transfer.createFilter(fromBlock=i, toBlock=(i + step - 1))
        events = filter.get_all_entries()
        if len(events) == 0:
            print("blocks" + str(i) + " to " + str(i + step) + " are empty of this contract")
            continue
        transaction_hash = ""
        for i in range(len(events)):
            #print(events[i])
            previous_transaction_hash = transaction_hash
            transaction_hash = (events[i]["transactionHash"]).hex()
            if transaction_hash == previous_transaction_hash:
                continue
            transaction = web3.eth.get_transaction(transaction_hash)
            input = (transaction["input"])
            if input[0:10] == cd.atomicMatch or input[0:10] == cd.buyPunk or transaction["to"] == cd.openSea:
                #print(event)
                #print(transaction)
                block_hash = (transaction["blockHash"]).hex()
                block = web3.eth.getBlock(block_hash)
                block_number = (transaction["blockNumber"])
                timestamp = block["timestamp"]
                wei_value = transaction["value"]
                ether_value = Web3.fromWei(wei_value, 'ether')
                #print(events[i])
                from_address = events[i]["args"]["from"]
                to_address = events[i]["args"]["to"]
                tokenID = transaction["input"][-5:]
                tokenID = int(tokenID, 16)
                #try:
                    #tokenURI = metadata_contract.functions.tokenURI(tokenID).call()
                #except:
                tokenURI = "punks_do_not_have_token_URIs"

                data = []
                data.append(contract_address)
                data.append(transaction_hash)
                data.append(str(block_number))
                data.append(str(timestamp))
                data.append(from_address)
                data.append(to_address)
                data.append(str(tokenID))
                data.append(str(tokenURI))
                data.append(str(ether_value))

                parsed = convert_list_to_transaction_json(data)

                save_to_firebase_new(transaction_hash, parsed)

                #print(data)

if __name__ == '__main__':
    # the relevant functions were called here, e.g.:
    # retrieve(cd.pudgyPenguinABI, cd.pudgyPenguinAddress, 12876000, 14000000, 1000)
    # retrieve_punks(6390000, 14000000, 10000)