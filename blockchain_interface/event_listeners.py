from web3 import Web3
import contract_details as cd
import time

import numpy as np 
import pandas as pd
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, db

#on each redeploy scan blocks starting from most recent database entry for each contract

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/15f211ab56884bfba42aba49864f6aa5', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

def update_firebase():
    cred_obj = firebase_admin.credentials.Certificate('key.json')
    app = firebase_admin.initialize_app(cred_obj, {'databaseURL':'https://practice-firebase-52292-default-rtdb.europe-west1.firebasedatabase.app/'})
    ref = db.reference('/newtest')
    print(ref.get())

def handle_event(event, contract, previous_hash = [" "]):
    print("=======================================")
    contract_address = event["address"]
    transaction_hash = (event["transactionHash"]).hex()
    if transaction_hash == previous_hash[0]:
        return
    previous_hash.pop()
    previous_hash.append(transaction_hash)
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
        if contract_address == cd.cloneXAddress or contract_address == cd.pudgyPenguinAddress or contract_address == cd.doodlesAddress:
            tokenID = transaction["input"][10 + (64 * 58):10 + (64 * 58) + 8]
        else:
            tokenID = transaction["input"][10 + (64 * 62):10 + (64 * 62) + 8]
        #print(contract_address)
        #print(tokenID)
        tokenID = int(tokenID, 16)
        tokenURI = contract.functions.tokenURI(tokenID).call()
        data = ""
        data += contract_address + "|" + transaction_hash + "|" + str(block_number) + "|" + str(timestamp) + "|"
        data += from_address + "|" + to_address + "|" + str(tokenID) + "|" + str(tokenURI) + "|" + str(ether_value) + "|" + "-"
        data += "\n"
        print(data)

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
    #append_to_lists(cd.cryptoPunkAddress, cd.cryptoPunkABI, contracts, event_filters)
    append_to_lists(cd.doodlesAddress, cd.doodlesABI, contracts, event_filters)
    append_to_lists(Web3.toChecksumAddress(cd.coolCatsAddress), cd.coolCatsABI, contracts, event_filters)
    append_to_lists(cd.cloneXAddress, cd.cloneXABI, contracts, event_filters)
    append_to_lists(cd.crypToadzAddress, cd.crypToadzABI, contracts, event_filters)
    append_to_lists(cd.boredApeKennelAddress, cd.boredApeKennelABI, contracts, event_filters)
    append_to_lists(cd.pudgyPenguinAddress, cd.pudgyPenguinABI, contracts, event_filters)

    log_loop(event_filters, contracts, 1)

if __name__ == '__main__':
    update_firebase()
    #start_listening()