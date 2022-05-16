import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
import re
import sys
import json
import requests
from ordered_set import OrderedSet

# pass in a column and return a dictionary of how frequently trait occurs 
# within column 
def find_frequency_of_value(column):
    # print(type(column))
    classes_set = OrderedSet(column)
    classes = np.array(list(classes_set))
    freq_labels = dict.fromkeys(classes, 0)
    for label in column:
        freq_labels[label] += 1

    return(freq_labels)