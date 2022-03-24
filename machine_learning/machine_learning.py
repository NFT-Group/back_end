import json
import requests
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout, LSTM
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
# import sys.path.append(.../machine_learning) #import retrieve_all_pickles_into_dict
# from ...retrieve_all_pickles_into_dict import retrieve_all_pickles_into_dict
from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict

#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error
import pickle

collection_dict = retrieve_all_pickles_into_dict()

preprocessed_df = collection_dict['boredape'].preprocessed_df

print(preprocessed_df)


def train_test_split(df, test_size=0.1, validation_size=0.1):
    df = df.sample(frac=1)
    train_split_row = len(df) - int((test_size + validation_size) * len(df))
    test_split_row = len(df) - int((test_size) * len(df))
    train_data = df.iloc[:train_split_row]
    test_data = df.iloc[test_split_row:]
    validation_data = df.iloc[train_split_row:test_split_row]
    return train_data, test_data, validation_data


test_size = 0.1
validation_size = 0.1
train, test, validation = train_test_split(preprocessed_df, test_size, validation_size)

X_train = train.drop(["ethprice"], axis = 1)

y_train = train["ethprice"]
X_test = test.drop(["ethprice"], axis = 1)
y_test = test["ethprice"]
X_validation = validation.drop(["ethprice"], axis = 1)
y_validation = validation["ethprice"]
# print(X_test)
# print(y_test)

model = Sequential()
model.add(Dense(13,activation='relu'))  
model.add(Dense(40,activation='relu'))
model.add(Dense(40,activation='relu'))
model.add(Dense(1))
## defining the optimiser and loss function
model.compile(optimizer='adam',loss='mse')
## training the model

print(type(X_train))
print(type(y_train))
print(type(X_validation))
print(type(y_validation))
X_train = np.asarray(X_train).astype(np.float32)
X_test = np.asarray(X_test).astype(np.float32)
y_train = np.asarray(y_train).astype(np.float32)
X_validation = np.asarray(X_validation).astype(np.float32)
y_validation = np.asarray(y_validation).astype(np.float32)
model.fit(x=X_train,y=y_train,
          validation_data=(X_validation,y_validation),
          batch_size=128,epochs=400)

preds = model.predict(X_test)
# print(y_test)
# print((y_test))
results = pd.DataFrame(preds, columns = ["predicted"])
results = results.values.tolist()
# y_test = y_test.values.tolist()
# results = pd.concat([results, y_test], axis=1)
# print(results)

print(mean_absolute_percentage_error(preds, y_test))
print(mean_absolute_error(preds, y_test))
print(preds)
print(y_test)