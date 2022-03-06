import pandas as pd
import numpy as np
import dateutil.parser

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

    # NORMALISE DATA WHICH NEEDS NORMALISING
    testable_data.running_sell_count = normalise(testable_data.running_sell_count.astype(float))
    testable_data.running_whale_weight = normalise(testable_data.running_whale_weight.astype(float))
    # doesn't work becauser it thinks it takes the column as a series 
    # rather than going element wise
    testable_data.timestamp = dateutil.parser.parse(testable_data.timestamp)


    print(testable_data)

    # RETURN

def normalise(column):
    normal_col = (column - column.min()) / (column.max() - column.min())
    return normal_col