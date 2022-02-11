from web3 import Web3
import requests
import contract_details as cd
import fs
import json
from pandas.io.json import json_normalize

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/15f211ab56884bfba42aba49864f6aa5'))
"""
def remove_json_whitespace(json_str):
    sm = 1
    index = 0
    new_json = ""
    for i in range(len(json_str)):
        if json_str[i] == '"':
            sm *= -1
        if sm == 1 and isspace(json_str[i]):
            continue
        else:
            new_json += json_str[index]
            index += 1
    return new_json
"""
def get_all_tokens(contract_abi, contract_address, start, end):
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    filename = "all_"
    filename += contract_address
    filename += ".csv"
    f = open(filename, "a")
    for i in range(start, end):
        tokenURI = contract.functions.tokenURI(i).call()
        if (tokenURI[0:4] == "ipfs"):
            tokenURI = "https://ipfs.io/ipfs/" + tokenURI[7:]	       
        r = requests.get(tokenURI)
        r = json.dumps(r.text, indent=None, separators=(",", ":"))
        r = r[1:-1]
        r = r.replace("\\n", "")
        r = r.replace ("\\", "")
        #r = remove_json_whitespace(r)
        #r = ''.join(r.split())
        data = str(i)
        data += "|"
        data += str(r)
        data += '\n'
        #f.write(data)
        print(data)
        print("success  " + tokenURI)

def get_cryptopunk_metadata(contract_abi, contract_address, start, end):
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    filename = "all_cryptopunk_metadata.csv"
    f = open(filename, "a")
    for i in range(start, end):
        metadata = contract.functions.punkAttributes(i).call()
        data = ""
        data += str(i)
        data += "|"
        data += metadata
        data += "\n"
        print(data)
        f.write(data)
        f.flush()
    f.close()

#get_all_tokens(cd.cloneXABI, cd.cloneXAddress, 1, 10)
get_cryptopunk_metadata(cd.cryptoPunkMDABI, cd.cryptoPunkMDAddress, 1000, 10000)
