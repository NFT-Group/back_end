import numpy as np 
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt 
from matplotlib import pyplot
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import re

def trait_format(data, json):
    trait_list = []
    for i in range(len(json)):
        for m in re.finditer('trait_type":"', json[i]):
            # print('found: ', m.start(), m.end())
            temp = (json[i])[m.end():m.end()+20]
            j = temp.find('"')
            trait_list.append(temp[:j])
    
    trait_set = set(trait_list)
    trait_list = list(trait_set)

    trait_found = np.zeros([len(json),len(trait_list)])

    for i in range(len(json)):
        for j in range(len(trait_list)):
            if(json[i].find(trait_list[j]) != -1):
                trait_found[i][j] = 1

    return trait_found

    # print(trait_found)
    # print(json[0])
    # print(trait_list)