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

#on each redeploy scan blocks starting from most recent database entry for each contract

## web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/15f211ab56884bfba42aba49864f6aa5', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/ce6bd1fdbecb4ad992ed224fd1b00694', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

def save_to_firebase_new(txnhash, dfjson):
    #ref = db.reference('/')
    #print("hash")
    #print(txnhash)
    #print("json")
    #print(dfjson[0])
    print(txnhash)
    ref.child(txnhash).set(dfjson[0])

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


def retrieve(contract_abi, contract_address, start, end, step):
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    for i in range(start, (end - step) + 1, step):
        filter = contract.events.Transfer.createFilter(fromBlock=i, toBlock=(i + step - 1))
        events = filter.get_all_entries()
        if len(events) == 0:
            continue
        transaction_hash = ""
        for i in range(len(events)):
            previous_transaction_hash = transaction_hash
            transaction_hash = (events[i]["transactionHash"]).hex()
            if transaction_hash == previous_transaction_hash:
                continue
            transaction = web3.eth.get_transaction(transaction_hash)
            input = (transaction["input"])
            if input[0:10] == cd.atomicMatch or input[0:10] == cd.buyPunk or transaction["to"] == cd.openSea:
                block_hash = (transaction["blockHash"]).hex()
                block = web3.eth.getBlock(block_hash)
                block_number = (transaction["blockNumber"])
                timestamp = block["timestamp"]
                wei_value = transaction["value"]
                ether_value = Web3.fromWei(wei_value, 'ether')
                from_address = "0x" + transaction["input"][2 + (32 * 5):2 + (32 * 5) + 40] #define in terms of 10 + 64*x blocks
                to_address = "0x" + transaction["input"][2 + (32 * 3):2 + (32 * 3) + 40] #also this
                tokenID_a = transaction["input"][10 + (64 * 58):10 + (64 * 58) + 8]
                tokenID_a = int(tokenID_a, 16)
                tokenID_b = transaction["input"][10 + (64 * 62):10 + (64 * 62) + 8]
                tokenID_b = int(tokenID_b, 16)
                tokenID = max(tokenID_a, tokenID_b)
                try:
                    tokenURI = contract.functions.tokenURI(tokenID).call()
                except:
                    tokenURI = "missing_token"

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

def retrieve_punks(start, end, step):
    contract_abi = cd.cryptoPunkABI
    contract_address = cd.cryptoPunkAddress
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    for i in range(start, (end - step) + 1, step):
        filter = contract.events.Transfer.createFilter(fromBlock=i, toBlock=(i + step - 1))
        events = filter.get_all_entries()
        if len(events) == 0:
            continue
        transaction_hash = ""
        for i in range(len(events)):
            previous_transaction_hash = transaction_hash
            transaction_hash = (events[i]["transactionHash"]).hex()
            if transaction_hash == previous_transaction_hash:
                continue
            transaction = web3.eth.get_transaction(transaction_hash)
            input = (transaction["input"])
            if input[0:10] == cd.atomicMatch or input[0:10] == cd.buyPunk or transaction["to"] == cd.openSea:
                block_hash = (transaction["blockHash"]).hex()
                block = web3.eth.getBlock(block_hash)
                block_number = (transaction["blockNumber"])
                timestamp = block["timestamp"]
                wei_value = transaction["value"]
                ether_value = Web3.fromWei(wei_value, 'ether')
                from_address = events[i]["args"]["from"]
                to_address = events[i]["args"]["to"]
                tokenID = transaction["input"][-5:]
                tokenID = int(tokenID, 16)
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


def handle_event(event, contract, previous_hash = [" "]):
    contract_address = event["address"]
    transaction_hash = (event["transactionHash"]).hex()
    if transaction_hash == previous_hash[0]:
        return
    previous_hash.pop()
    previous_hash.append(transaction_hash)
    transaction = web3.eth.get_transaction(transaction_hash)
    input = (transaction["input"])
    print(event)
    print(transaction)
    if input[0:10] == cd.atomicMatch or input[0:10] == cd.buyPunk or transaction["to"] == cd.openSea:
        #print(event)
        #print(transaction)
        print("ATOMIC MATCH")
        block_hash = (transaction["blockHash"]).hex()
        block = web3.eth.getBlock(block_hash)
        block_number = (transaction["blockNumber"])
        timestamp = block["timestamp"]
        wei_value = transaction["value"]
        ether_value = Web3.fromWei(wei_value, 'ether')
        
        tokenURI = None
        tokenID = None
        if contract_address == cd.cryptoPunkAddress:
            from_address = transaction["input"][2 + (32 * 5):2 + (32 * 5) + 40] #define in terms of 10 + 64*x blocks
            to_address = transaction["input"][2 + (32 * 3):2 + (32 * 3) + 40] #also this
            tokenID = transaction["input"][-5:]
            tokenID = int(tokenID_a, 16)
            tokenURI = "punks_do_not_have_token_URIs"
        else:
            from_address = "0x" + transaction["input"][2 + (32 * 5):2 + (32 * 5) + 40] #define in terms of 10 + 64*x blocks
            to_address = "0x" + transaction["input"][2 + (32 * 3):2 + (32 * 3) + 40] #also this
            tokenID_a = transaction["input"][10 + (64 * 58):10 + (64 * 58) + 8]
            tokenID_a = int(tokenID_a, 16)
            tokenID_b = transaction["input"][10 + (64 * 62):10 + (64 * 62) + 8]
            tokenID_b = int(tokenID_b, 16)
            tokenID = max(tokenID_a, tokenID_b)
            try:
                tokenURI = contract.functions.tokenURI(tokenID).call()
            except:
                tokenURI = "missing_token"
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

        #save_to_firebase_new(transaction_hash, parsed)

def log_loop(event_filters, contracts, poll_interval):
    while True:
        for event_filter, contract in zip(event_filters, contracts):
            for event in event_filter.get_new_entries():
                handle_event(event, contract)
        time.sleep(poll_interval)

def append_to_lists(contract_address, contract_abi, contracts, event_filters):
    event_filters.append(web3.eth.filter({'fromBlock':'latest', 'address':contract_address}))
    contracts.append(web3.eth.contract(abi=contract_abi, address=contract_address))

def start_listening():
    contracts = []
    event_filters = []
    append_to_lists(cd.apeAddress, cd.apeABI, contracts, event_filters)
    append_to_lists(cd.cryptoPunkAddress, cd.cryptoPunkABI, contracts, event_filters)
    append_to_lists(cd.doodlesAddress, cd.doodlesABI, contracts, event_filters)
    append_to_lists(Web3.toChecksumAddress(cd.coolCatsAddress), cd.coolCatsABI, contracts, event_filters)
    append_to_lists(cd.cloneXAddress, cd.cloneXABI, contracts, event_filters)
    append_to_lists(cd.crypToadzAddress, cd.crypToadzABI, contracts, event_filters)
    append_to_lists(cd.boredApeKennelAddress, cd.boredApeKennelABI, contracts, event_filters)
    append_to_lists(cd.pudgyPenguinAddress, cd.pudgyPenguinABI, contracts, event_filters)

    log_loop(event_filters, contracts, 1)

"""
def update_firebase():
    cred_obj = firebase_admin.credentials.Certificate('key.json')
    app = firebase_admin.initialize_app(cred_obj, {'databaseURL':'https://practice-firebase-52292-default-rtdb.europe-west1.firebasedatabase.app/'})
    ref = db.reference('/newtest')
    print(ref.get())

"""

if __name__ == '__main__':

    ## find latest firebase allCollections block number (a)

    #latest_firebase_block = ref.order_by_child('blocknumber').limit_to_first(100).get()
    #for i in range(len(list(latest_firebase_block.keys()))):
        #result = latest_firebase_block[list(latest_firebase_block.keys())[i]]#['blocknumber']
        #print(result)
    
    latest_firebase_block = ref.order_by_child('blocknumber').limit_to_last(1).get()
    latest_firebase_block = latest_firebase_block[list(latest_firebase_block.keys())[0]]['blocknumber']
    print(latest_firebase_block)

    latest_firebase_block += 1

    
    block = web3.eth.get_block('latest')
    latest_block_number = block['number']
    print("old latest block")
    print(latest_block_number)

    catch_up_speed = 1000

    while (((latest_block_number - latest_firebase_block) % catch_up_speed) != 0):
        latest_firebase_block -= 1

    print("new latest firebase block")
    print(latest_firebase_block)

    ## scan from a to b for all 8 collections
    retrieve(cd.apeABI, cd.apeAddress, latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve(cd.boredApeKennelABI, cd.boredApeKennelAddress, latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve(cd.doodlesABI, cd.doodlesAddress, latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve(cd.coolCatsABI, Web3.toChecksumAddress(cd.coolCatsAddress), latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve(cd.cloneXABI, cd.cloneXAddress, latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve(cd.crypToadzABI, cd.crypToadzAddress, latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve(cd.pudgyPenguinABI, cd.pudgyPenguinAddress, latest_firebase_block, latest_block_number, catch_up_speed)
    retrieve_punks(latest_firebase_block, latest_block_number, catch_up_speed)
    ## find latest ethereum chain block number again (c)
    block = web3.eth.get_block('latest')
    REAL_latest_block_number = block['number']
    print("REAL latest block")
    print(REAL_latest_block_number)
    while (latest_block_number != REAL_latest_block_number):
        temp_block_number = latest_block_number
        latest_block_number = REAL_latest_block_number

        retrieve(cd.apeABI, cd.apeAddress, temp_block_number, REAL_latest_block_number, 1)
        retrieve(cd.boredApeKennelABI, cd.boredApeKennelAddress, temp_block_number, REAL_latest_block_number, 1)
        retrieve(cd.doodlesABI, cd.doodlesAddress, temp_block_number, REAL_latest_block_number, 1)
        retrieve(cd.coolCatsABI, Web3.toChecksumAddress(cd.coolCatsAddress), temp_block_number, REAL_latest_block_number, 1)
        retrieve(cd.cloneXABI, cd.cloneXAddress, temp_block_number, REAL_latest_block_number, 1)
        retrieve(cd.crypToadzABI, cd.crypToadzAddress, temp_block_number, REAL_latest_block_number, 1)
        retrieve(cd.pudgyPenguinABI, cd.pudgyPenguinAddress, temp_block_number, REAL_latest_block_number, 1)
        retrieve_punks(temp_block_number, REAL_latest_block_number, 1)

        block = web3.eth.get_block('latest')
        REAL_latest_block_number = block['number']
        print("REAL_latest_block_number")
        print(REAL_latest_block_number)

        
        ## scan from a to b for all 8 collections
        
        ## find latest ethereum chain block number again (c)
       
        ## if (c) != (b), go back to scan step, otherwise continue
    ## start scanning live

    print("starting to listen!")
    start_listening() #make sure this writes!!
