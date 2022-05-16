import pathlib
import numpy as np
import csv
csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

def clean_null_data_transactions_data(transactions_link, collection_id):
    # import the blockchain csv file and split it into data and traits
    f = open(str(pathlib.Path(__file__).parent.resolve()) + 
        '/data/clean_transactions/' + collection_id + '.csv', "w")
    writer = csv.writer(f, dialect='piper')
    for line in open(transactions_link):
            temp = line.strip().split("|")
            if(temp[4] == '0x0000000000000000000000000000000000000000' or 
                temp[-1] == '0'):
                continue
            writer.writerow(temp)
    f.close()
