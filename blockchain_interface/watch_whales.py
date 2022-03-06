import numpy as np 
import pandas as pd
from datetime import datetime
import json
from web3 import Web3
#from web3.auto import w3
import requests
import contract_details as cd
import fs

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/1c06ca684f954cfa9c43e80b9112cb8f', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

def watch_whales():
    addresses = []
    for line in open("whale_wallets.txt"):
        #line.replace("\n", "")
        #line.replace(",", "")
        addresses.append(line[:-2])
    block = None
    last_block = ""
    latest_block = web3.eth.getBlock('latest')["number"]
    next_block = latest_block
    while (True):
        latest_block = web3.eth.getBlock('latest')["number"]
        #print("latest block:")
        #print(latest_block)
        #print("next block:")
        #print(next_block)
        #print("last block:")
        #print(last_block)
        if (next_block < latest_block) or (next_block == latest_block and next_block != last_block):
            try:
                block = web3.eth.get_block(next_block, full_transactions=True)
            except:
                continue #should try again
            #print(block)
            print(block["number"])
            for i in range(len(block["transactions"])):
                #print(i)
                txn = block["transactions"][i]
                input = txn["input"]
                if (txn["to"] == cd.openSea and input[0:10] == cd.atomicMatch):
                    from_address = "0x" + txn["input"][2 + (32 * 5):2 + (32 * 5) + 40] #define in terms of 10 + 64*x blocks
                    to_address = "0x" + txn["input"][2 + (32 * 3):2 + (32 * 3) + 40] #also this
                    if (from_address in addresses):
                        print("WHALE ACTIVITY")
                        print(txn)
                    if(to_address in addresses):
                        print("WHALE ACTIVITY")
                        print(txn)
            last_block = next_block
            next_block += 1
            


if __name__ == '__main__':
    watch_whales()

#14230000