import pandas as pd
import numpy as np
import dateutil.parser
from datetime import datetime
import time
import calendar

def preprocess(collection_df):

    # REMOVED ROWS WHICH HAVE GARABAGE VALUES
    collection_df = collection_df[
        collection_df.fromaddress != '0x0000000000000000000000000000000000000000']
    collection_df = collection_df[
        collection_df.ethprice != '0.00']

    # REMOVE COLUMNS WHICH WON'T BE USED
    testable_data = collection_df.drop([
        'tokenid',
        'fromaddress', 
        'toaddress', 
        'tokenuri',
        'transactionhash',
        'blocknumber',
        'contracthash'
        ], axis=1)

    now = datetime.now()
    testable_data.timestamp = pd.to_datetime(testable_data.timestamp)
    testable_data.timestamp = now - testable_data.timestamp
    testable_data.timestamp = testable_data.timestamp.apply(lambda x: x.total_seconds())

    # NORMALISE DATA WHICH NEEDS NORMALISING
    testable_data.running_sell_count = normalise(testable_data.running_sell_count.astype(float))
    testable_data.running_whale_weight = normalise(testable_data.running_whale_weight.astype(float))
    # although the following line normalise time data, is there a way we can 
    # give more weight to closer times and dates than farther ones?
    testable_data.timestamp = normalise(testable_data.timestamp.astype(float))

    example = '2021-11-15'
    example_new = datetime.strptime(example, "%Y-%m-%d")
    now = datetime.now()
    difference = now - example_new

    print(type(difference))
    print(now)
    print(example_new)
    


    print(testable_data)

    # RETURN

def normalise(column):
    normal_col = (column - column.min()) / (column.max() - column.min())
    return normal_col