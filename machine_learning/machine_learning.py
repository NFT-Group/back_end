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
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error
import pickle




def train_test_split(df, test_size=0.1, validation_size=0.1):
    df = df.sample(frac=1)
    train_split_row = len(df) - int((test_size + validation_size) * len(df))
    test_split_row = len(df) - int((test_size) * len(df))
    train_data = df.iloc[:train_split_row]
    test_data = df.iloc[test_split_row:]
    validation_data = df.iloc[train_split_row:test_split_row]
    return train_data, test_data, validation_data


def neural_network_model_tensor(preprocessed_df):
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
    
    f.write("\nMean absolute percentage error is: ")
    f.write(f"{(mean_absolute_percentage_error(y_test, preds))}")
    f.write("\nMean absolute error is: ")
    f.write(f"{(mean_absolute_error(y_test, preds))}")
    f.write("\nMean squared error is: ")
    f.write(f"{(mean_squared_error(y_test, preds))}")
    print(preds)
    print(y_test)


f = open("JC_working_folder/Performance_measures_of_nn.txt", 'w')
    
collection_dict = retrieve_all_pickles_into_dict()
for name in collection_dict:
    try:
        preprocessed_df = collection_dict[name].preprocessed_df
        print(preprocessed_df)
        f.write("\n")
        f.write(name)
        neural_network_model_tensor(preprocessed_df)
    except:
        print("error")
