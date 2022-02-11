from web3 import Web3
import contract_details as cd
import time

web3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/1c06ca684f954cfa9c43e80b9112cb8f', websocket_timeout=100, websocket_kwargs={'max_size': 1000000000}))

#web3 = websockets.client.WebSocketClientProtocol('wss://mainnet.infura.io/ws/v3/bba210d6663b4c0999d9ccb2c34a91bd', max_size=1000000)

def retrieve_small(contract_abi, contract_address, start, end):
    filename = ""
    filename = "past_" + contract_address + ".csv"
    #f = open(filename, "a")
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)
    filter = contract.events.Transfer.createFilter(fromBlock=start, toBlock=end)
    events = filter.get_all_entries()
    if len(events) == 0:
        print("blocks" + str(i) + " to " + str(i + step) + " are empty of this contract")
        return
    transaction_hash = ""
    for i in range(len(events)):
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
            #f.write(data)

def retrieve(contract_abi, contract_address, start, end, step):
    filename = ""
    filename = "past_" + contract_address + ".csv"
    f = open(filename, "a")
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
                f.write(data)
                print(block_number)
    f.close()

def retrieve_punks(start, end, step):
    contract_abi = cd.cryptoPunkABI
    contract_address = cd.cryptoPunkAddress
    filename = ""
    filename = "past_" + contract_address + ".csv"
    f = open(filename, "a")
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
                from_address = "0x" + events[i]["args"]["from"]
                to_address = "0x" + events[i]["args"]["to"]
                tokenID = transaction["input"][-5:]
                tokenID = int(tokenID, 16)
                #try:
                    #tokenURI = metadata_contract.functions.tokenURI(tokenID).call()
                #except:
                tokenURI = "punks_do_not_have_token_URIs"
                data = ""
                data += contract_address + "|" + transaction_hash + "|" + str(block_number) + "|" + str(timestamp) + "|"
                data += from_address + "|" + to_address + "|" + str(tokenID) + "|" + str(tokenURI) + "|" + str(ether_value) + "|" + "-"
                data += "\n"
                f.write(data)
                print(block_number)
                #print(data)
    f.close()

if __name__ == '__main__':
    #retrieve(cd.pudgyPenguinABI, cd.pudgyPenguinAddress, 12876000, 14000000, 1000)
    #retrieve_small(cd.cryptoPunkABI, cd.cryptoPunkAddress, 13980000, 14000000)
    retrieve_punks(6393000, 14000000, 1000)