import json
import requests
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout, LSTM

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_percentage_error
import pickle

preprocessed_df = pd.read_pickle("apes_preprocessed_df.pkl")
# print(preprocessed_df)


def train_test_split(df, test_size=0.1, validation_size=0.1):
    df = df.sample(frac=1)
    train_split_row = len(df) - int((test_size + validation_size) * len(df))
    test_split_row = len(df) - int((test_size) * len(df))
    train_data = df.iloc[:train_split_row]
    test_data = df.iloc[test_split_row:]
    validation_data = df.iloc[train_split_row:test_split_row]
    return train_data, test_data, validation_data

# # def extract_window_data(df, window_len=5, zero_base=True):
# #     window_data = []
# #     for idx in range(len(df) - window_len):
# #         tmp = df[idx: (idx + window_len)].copy()
# #         if zero_base:
# #             tmp = normalise_zero_base(tmp)
# #         window_data.append(tmp.values)
# #     return np.array(window_data)

# # def prepare_data(df, target_col, window_len=10, zero_base=True, test_size=0.2):
# #     train_data, test_data = train_test_split(df, test_size=test_size)
# #     X_train = extract_window_data(train_data, window_len, zero_base)
# #     X_test = extract_window_data(test_data, window_len, zero_base)
# #     y_train = train_data[target_col][window_len:].values
# #     y_test = test_data[target_col][window_len:].values
# #     if zero_base:
# #         y_train = y_train / train_data[target_col][:-window_len].values - 1
# #         y_test = y_test / test_data[target_col][:-window_len].values - 1

#     # return train_data, test_data, X_train, X_test, y_train, y_test

# def build_nn_model(input_data, output_size, neurons=100, activ_func='linear',
#                      dropout=0.2, loss='mse', optimizer='adam'):
#     model = Sequential()
#     print(input_data.shape)
#     model.add(LSTM(neurons, input_shape=(input_data.shape[0], input_data.shape[1])))
#     model.add(Dropout(dropout))
#     model.add(Dense(units=output_size))
#     model.add(Activation(activ_func))

#     model.compile(loss=loss, optimizer=optimizer)
#     return model

# np.random.seed(42)
# window_len = 5
# zero_base = True
# lstm_neurons = 100
# epochs = 20
# batch_size = 32
# loss = 'mse'
# dropout = 0.2
# optimizer = 'adam'

# # train, test, X_train, X_test, y_train, y_test = prepare_data(
# #     hist, target_col, window_len=window_len, zero_base=zero_base, test_size=test_size)
# X_train = train.drop(["ethprice"], axis = 1)
# y_train = train["ethprice"]
# X_test = test.drop(["ethprice"], axis = 1)
# y_test = test["ethprice"]

# X_train = tf.convert_to_tensor(X_train)
# y_train = tf.convert_to_tensor(y_train)
# X_test = tf.convert_to_tensor(X_test)
# y_test = tf.convert_to_tensor(y_test)
# print(X_train)
# print("X test is", X_test)
# print("Y test is ", y_test)
# model = build_lstm_model(
#     X_train, output_size=1, neurons=lstm_neurons, dropout=dropout, loss=loss,
#     optimizer=optimizer)
# history = model.fit(
#     X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True)

# # targets = test[target_col][window_len:]
# preds = model.predict(X_test).squeeze()
# print(mean_absolute_error(preds, y_test))

test_size = 0.1
validation_size = 0.1
train, test, validation = train_test_split(preprocessed_df, test_size, validation_size)

X_train = train.drop(["ethprice"], axis = 1)
y_train = train["ethprice"]
X_test = test.drop(["ethprice"], axis = 1)
y_test = test["ethprice"]
X_validation = validation.drop(["ethprice"], axis = 1)
y_validation = validation["ethprice"]
print(X_test)
print(y_test)
# define base model
# print(X_train.shape)
# def baseline_model():
# 	# create model
# 	model = Sequential()
# 	model.add(Dense(12, input_dim=12, kernel_initializer='normal', activation='relu'))
# 	model.add(Dense(1, kernel_initializer='normal'))
# 	# Compile model
# 	model.compile(loss='mean_squared_error', optimizer='adam')
# 	return model
# # evaluate model
# estimator = Ski-Keras(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)
# kfold = KFold(n_splits=10)
# results = cross_val_score(estimator, X_train, y_train, cv=kfold)
# print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))

model = Sequential()
model.add(Dense(12,activation='relu'))  
model.add(Dense(20,activation='relu'))
model.add(Dense(20,activation='relu'))
model.add(Dense(1))
## defining the optimiser and loss function
model.compile(optimizer='adam',loss='mse')
## training the model
model.fit(x=X_train,y=y_train,
          validation_data=(X_validation,y_validation),
          batch_size=128,epochs=1)

preds = model.predict(X_test)
print(y_test)
print((y_test))
results = pd.DataFrame(preds, columns = ["predicted"])
results = results.values.tolist()
y_test = y_test.values.tolist()
results = results
results = pd.concat([results, y_test], axis=1)
print(results)

print(mean_absolute_percentage_error(preds, y_test))