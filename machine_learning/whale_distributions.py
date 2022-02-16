import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
import re
import sys
import json
import requests
from ordered_set import OrderedSet
import pathlib
from trait_distribution import find_frequency_of_value

def whale_distributions(transactions_link):
    transactions_data = []
    transactions_json = []
    transactions_whole_set = []

    # import the blockchain csv file and split it into data and traits
    for line in open(transactions_link):
            temp = line.strip().split("|")
            transactions_whole_set.append(temp)
            transactions_json.append(temp[-1])
            transactions_data.append(temp[:-1])

    transactions_data = np.array(transactions_data, dtype=object)

    frequency_of_sellers = find_frequency_of_value(transactions_data[:,4])
    frequency_of_buyers = find_frequency_of_value(transactions_data[:,5])
    frequency_of_purchases = find_frequency_of_value(transactions_data[:,6])

    sorted_sellers = {k: v for k, v in sorted(frequency_of_sellers.items(), key = lambda item: item[1])}
    sorted_buyers = {k: v for k, v in sorted(frequency_of_buyers.items(), key = lambda item: item[1])}
    sorted_purchases = {k: v for k, v in sorted(frequency_of_purchases.items(), key = lambda item: item[1])}



    # print(sorted_purchases)
    print(sorted_buyers)



    










apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

# cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'

coolCatsAddress = '0x1a92f7381b9f03921564a437210bb9396471050c'

# cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'

cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'

crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'

boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'

pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'


value = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
transactions_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/historical/past_' + value + '.csv'
unique_nfts_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/transactions/all_' + value + '.csv'

whale_distributions(transactions_link)