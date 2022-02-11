import numpy as np
from numpy import genfromtxt
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt 
from matplotlib import pyplot
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from traitFormat import trait_format
from rarity import sim
from rarity import individual_rar
from rarity import list_rar
from datetime import datetime
import csv
import sys

def lookup_eth_price(date, eth_usd_csv):
        eth_usd_csv = np.asarray(eth_usd_csv)
#       print(eth_usd_csv)
        for i in range(len(eth_usd_csv)):
                if date == eth_usd_csv[i][0]:
                        return eth_usd_csv[i][4]

def add_real_usd_prices(data):



    purchase_date = []
    eth_price = []
    # print(type(data))
    # loop for retrieving timestamp and eth price of every transaction
    for i in range(len(data)):
            time_temp = int(data[i][3])
            time_temp = datetime.utcfromtimestamp(time_temp).strftime('%Y-%m-%d')
            purchase_date.append(time_temp)
            eth_temp = float(data[i][8])
            eth_price.append(eth_temp)

    purchase_date = np.asarray(purchase_date)
    eth_price = np.asarray(eth_price)

    # open historical eth-usd csv file for lookup
    eth_usd_csv = genfromtxt('/home/tm21/ML/regression/ETH-USD_1_.csv', delimiter=",", encoding="utf-8", dtype=None)


    date_eth_price = []
    for i in range(len(purchase_date)):
            date_eth_price_temp = float(lookup_eth_price(purchase_date[i], eth_usd_csv))
            date_eth_price.append(date_eth_price_temp)
    date_eth_price = np.asarray(date_eth_price)

    # this will be the price of each transaction in eth times the exchange rate or ETH/USD on the date of transaction
    price_of_transaction_in_USD = eth_price * date_eth_price
#     print(np.shape(data))
#     print(price_of_transaction_in_USD)
    data = np.column_stack((data,price_of_transaction_in_USD)) 
    # now we need to change that price into one for real usd price
#     print(np.shape(data))     

#     print(data[:10,])
    
    return data