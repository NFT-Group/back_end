import numpy as np
from numpy import genfromtxt
from numpy import arange

import pathlib
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt 
from matplotlib import pyplot
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import ElasticNetCV
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import RepeatedKFold
from sklearn import metrics

import warnings


from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error

from trait_format import trait_format
from datetime import datetime
import csv
import sys
import json
import math
from add_real_usd_prices import add_real_usd_prices
from trait_distribution import trait_distribution
from match_trait_dis_values import match_trait_dis_values
from whale_distributions import whale_distributions
from clean_null_data import clean_null_data_transactions_data

from ordered_set import OrderedSet


warnings.filterwarnings("ignore")

def sell_count(transactions_data):
        unique_id = OrderedSet(transactions_data[:,-4])
        unique_id = np.array(list(unique_id), dtype=int)
        transactions_data_id_list = np.array(transactions_data[:,-4], dtype=int)
        sell_count_array = np.zeros([len(transactions_data),1])

        count_dict = dict.fromkeys(unique_id, 0)

        for row in range(len(unique_id)):
                for i, j in zip(range(len(transactions_data_id_list)), range(len(sell_count_array))):
                        if(unique_id[row] == transactions_data_id_list[i]):
                                count_dict[unique_id[row]] += 1
                                sell_count_array[i,0] = count_dict[unique_id[row]]
       

        print("SELL COUNT ARRAY: ", sell_count_array)
        return sell_count_array


def data_combining_and_structuring(transactions_link, unique_nfts_link):
        transactions_data = []
        transactions_json = []
        transactions_whole_set = []

        unique_data = []
        unique_json = []
        unique_whole_set = []

        # import the blockchain csv file and split it into data and traits
        for line in open(transactions_link):
                temp = line.strip().split("|")
                transactions_whole_set.append(temp)
                transactions_json.append(temp[-1])
                transactions_data.append(temp[:-1])

        for line in open(unique_nfts_link):
                temp = line.strip().split("|")
                unique_data.append(temp[0])
                json_temp = json.loads(temp[1])
                try:
                        unique_json.append(json.dumps(json_temp["attributes"]))
                except KeyError:
                        continue
        # print(unique_json[0])

        unique_header_list, trait_values_distribution = trait_distribution(unique_data, unique_json)
        
        transactions_data = add_real_usd_prices(transactions_data)
        final_column = transactions_data.shape[1]-1

        sell_counter = sell_count(transactions_data)
        assert transactions_data.shape[0] == sell_counter.shape[0]
        transactions_data = np.column_stack((transactions_data, sell_counter))

        # print(type(transactions_data))
        current_seller_weight = whale_distributions(transactions_data)
        # print(transactions_data.shape)
        # print(current_seller_weight.shape)
        assert transactions_data.shape[0] == current_seller_weight.shape[0]
        transactions_data = np.column_stack((transactions_data, current_seller_weight))

        # print(transactions_data)
        # print(final_column)
        my_temp_set = OrderedSet(unique_header_list)
        
        transactions_data = match_trait_dis_values(transactions_data, trait_values_distribution, final_column, unique_header_list)
        # transactions_data.to_csv('out_data', index = False)
        trait_headers = list(my_temp_set)

        return(transactions_data, trait_headers)

def get_test_train_data(data, train_columns_string):
        data["priceInETH"] = pd.to_numeric(data['priceInETH'], downcast = "float")
        data = data[data.priceInETH != 0.0]
        # data.to_csv('out_data_0.csv', index = False)
        predict_column='priceInETH'
        x = data[train_columns_string]
        y = data[predict_column]
        return (train_test_split(x, y, test_size=0.10,shuffle=False))

def analyse_results(y_pred, y_test):
        #MSE
        from sklearn import metrics
        print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        #MAPE
        def mean_absolute_percentage_error(y_test, y_pred):
                y_test = y_test.astype('float')
                # print(y_test)
                y_pred = y_pred.astype('float')
                y_test, y_pred = np.array(y_test), np.array(y_pred)
                return np.mean(np.abs((y_test - y_pred)/y_test)) * 100

        print('MAPE:', mean_absolute_percentage_error(y_test, y_pred))

        # for positive results coefficient of variation is a good measure to compare different models
        # print('Coefficient of variation: ', metrics.mean_squared_error/metrics.mean)


def linear_regression(x_train, x_test, y_train, y_test):
        
        LR = LinearRegression()  # create object for the class
        LR.fit(x_train, y_train)  # perform linear regression
        y_pred = LR.predict(x_test)
        return(y_pred, y_test)
        # print("Training set accuracy = " + str(LR.score(x_train, y_train)))
        # print("Test set accuracy = " + str(LR.score(x_test, y_test)))

        # #MSE
        # from sklearn import metrics
        # print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        # #MAPE
        # def mean_absolute_percentage_error(y_test, y_pred):
        #         y_test = y_test.astype('float')
        #         print(y_test)
        #         y_pred = y_pred.astype('float')
        #         y_test, y_pred = np.array(y_test), np.array(y_pred)
        #         return np.mean(np.abs((y_test - y_pred)/y_test)) * 100

        # print('MAPE:', mean_absolute_percentage_error(y_test, y_pred))
        

def neural_networks(x_train, x_test, y_train, y_test):

        MLP = MLPRegressor(hidden_layer_sizes=(10), activation='tanh', solver='lbfgs')
        MLP.fit(x_train, y_train)
        #MLP = MLPRegressor(random_state=1, max_iter=500).fit(x_train, y_train)
        print("Prediction of x_test is")
        print(MLP.predict(x_test[:2]))
        # MLP = MLPRegressor(hidden_layer_sizes = (200, 200, 200, 200, 200), activation = 'relu', solver = 'adam', max_iter = 500, learning_rate = 'adaptive')  # create object for the class
        MLP.fit(x_train, y_train)  # perform linear regression
        y_pred = MLP.predict(x_test)
        return(y_pred, y_test)

        # # compare y_pred vs y_test
        # y_test_vs_pred = np.zeros((len(y_test),2))
        # y_test_vs_pred[:, 0] = y_test
        # y_test_vs_pred[:, 1] = y_pred
        # print("Actual vs prediction ")
        # print(y_test_vs_pred)

        # # testSet = pd.concat([X_test, y_test], axis = 1)

        # # datasetPredict = pd.concat([testSet.reset_index(), pd.Series(y_pred, name = 'PredictedGenPrice')], axis = 1).round(2)
        
        # # datasetPredict.corr()
        # print("Training set accuracy = " + str(MLP.score(x_train, y_train)))
        # print("Test set accuracy = " + str(MLP.score(x_test, y_test)))

        # #MSE
        # from sklearn import metrics
        # print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        # #MAPE
        # def mean_absolute_percentage_error(y_test, y_pred):
        #         y_test = y_test.astype('float')
        #         print(y_test)
        #         y_pred = y_pred.astype('float')
        #         y_test, y_pred = np.array(y_test), np.array(y_pred)
        #         return np.mean(np.abs((y_test - y_pred)/y_test)) * 100

        # print('MAPE:', mean_absolute_percentage_error(y_test, y_pred))


# @ignore_warnings(category=ConvergenceWarning)

def elastic_net(x_train, x_test, y_train, y_test):

        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        # define model
        ratios = arange(0, 1, 0.01)
        alphas = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]
        EN = ElasticNetCV(l1_ratio=ratios, alphas=alphas, cv=cv, n_jobs=-1)
        # EN = ElasticNet(alpha=1.0, l1_ratio=0.5)
        EN.fit(x_train, y_train)
        print("Prediction of x_test is")
        print(EN.predict(x_test[:2]))
        EN.fit(x_train, y_train)  # perform linear regression
        y_pred = EN.predict(x_test)
        return(y_pred, y_test)

        # # compare y_pred vs y_test
        # y_test_vs_pred = np.zeros((len(y_test),2))
        # y_test_vs_pred[:, 0] = y_test
        # y_test_vs_pred[:, 1] = y_pred
        # print("Actual vs prediction ")
        # print(y_test_vs_pred)

        # # testSet = pd.concat([X_test, y_test], axis = 1)

        # # datasetPredict = pd.concat([testSet.reset_index(), pd.Series(y_pred, name = 'PredictedGenPrice')], axis = 1).round(2)
        
        # # datasetPredict.corr()
        # print("Training set accuracy = " + str(EN.score(x_train, y_train)))
        # print("Test set accuracy = " + str(EN.score(x_test, y_test)))

        # #MSE
        # print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        # #MAPE
        # def mean_absolute_percentage_error(y_test, y_pred):
        #         y_test = y_test.astype('float')
        #         print(y_test)
        #         y_pred = y_pred.astype('float')
        #         y_test, y_pred = np.array(y_test), np.array(y_pred)
        #         return np.mean(np.abs((y_test - y_pred)/y_test)) * 100

        # print('MAPE:', mean_absolute_percentage_error(y_test, y_pred))
        # print('Alpha: %f' % EN.alpha_)
        # print('l1_ratio_: %f' % EN.l1_ratio_)


def random_forest_reg(x_train, x_test, y_train, y_test):
        train_error=[]
        test_error=[]
        minDepth=20
        maxDepth=40
        models=[]
        for depth in range(minDepth,maxDepth,5):
                regr=RandomForestRegressor(max_depth=depth, random_state=0,n_estimators=5,verbose=2)
                regr.fit(x_train, y_train)
                models.append(regr)
                tr_error=math.sqrt(mean_squared_error(regr.predict(x_train),y_train))
                te_error=math.sqrt(mean_squared_error(regr.predict(x_test),y_test))
                test_error.append(tr_error)
                train_error.append(te_error)
                print (depth,tr_error,te_error)
        # train_plot=pd.DataFrame(train_error,index=range(20,40,5),columns=["test_Data"])
        # test_plot=pd.DataFrame(test_error,index=range(20,40,5),columns=["train_Data"])
        # plotdata=pd.concat([train_plot,test_plot],axis=1)
        # plotdata.plot()
        # x_test.size
        y_pred = regr.predict(x_test)
        return(y_pred, y_test)
        # # compare y_pred vs y_test
        # y_test_vs_pred = np.zeros((len(y_test),2))
        # y_test_vs_pred[:, 0] = y_test
        # y_test_vs_pred[:, 1] = y_pred
        # print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        # print("Actual vs prediction ")
        # print(y_test_vs_pred)
        # np.savetxt("forest_test_vs_prediction.csv", y_test_vs_pred, delimiter=",")
# linear_regression(transactions_link, unique_nfts_link)
# neural_networks(transactions_link, unique_nfts_link)
# elastic_net("out_data.csv")




def run_regressions(data, headers, name):
        x_train, x_test, y_train, y_test = get_test_train_data(data, headers)
        print("\n---------- Linear regression ----------\n")
        y_pred, y_test = linear_regression(x_train, x_test, y_train, y_test)
        analyse_results(y_pred, y_test)
        print("\n---------- Elastic Net ----------\n")
        y_pred, y_test = elastic_net(x_train, x_test, y_train, y_test)
        analyse_results(y_pred, y_test)
        print("\n---------- Random Forest ----------\n")
        y_pred, y_test = random_forest_reg(x_train, x_test, y_train, y_test)
        analyse_results(y_pred, y_test)
        save_y_predict_vs_test(y_test, y_pred, name)

def save_y_predict_vs_test(y_test, y_pred, name):
        y_test_vs_pred = np.zeros((len(y_test),2))
        y_test_vs_pred[:, 0] = y_test
        y_test_vs_pred[:, 1] = y_pred
        name = name + ".csv"
        np.savetxt(name, y_test_vs_pred, delimiter=",")

def create_data(transactions_link, unique_nfts_link, name):
        data, trait_headers = data_combining_and_structuring(transactions_link, unique_nfts_link)
        print(trait_headers)
        headers = trait_headers
        headers.extend(['numberOfTraits', 'blockNumber', 'timestamp'])
        print(headers)
        run_regressions(data, trait_headers, name)





apeAddress = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

# cryptoPunkMDAddress = '0x16F5A35647D6F03D5D3da7b35409D65ba03aF3B2'
doodlesAddress = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'

coolCatsAddress = '0x1a92f7381b9f03921564a437210bb9396471050c'

# cryptoKittiesAddress = '0x06012c8cf97bead5deae237070f9587f8e7a266d'

cloneXAddress = '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B'

crypToadzAddress = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'

boredApeKennelAddress = '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623'

pudgyPenguinAddress = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'



collection_addresses_dict = {'apeAddress': apeAddress, "doodlesAddress": doodlesAddress,
        "coolCatsAddress": coolCatsAddress,
        "cloneXAddress": cloneXAddress, "crypToadzAddress": crypToadzAddress,
        "boredApeKennelAddress": boredApeKennelAddress, "pudgyPenguinAddress": pudgyPenguinAddress}

for value in collection_addresses_dict.values():
        transactions_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/historical/past_' + value + '.csv'
        # unique_nfts_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/transactions/all_' + value + '.csv'
        clean_null_data_transactions_data(transactions_link, value)

for value in collection_addresses_dict.values():
        transactions_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/clean_transactions/' + value + '.csv'
        unique_nfts_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/complete/all_' + value + '.csv'
        print(transactions_link)
        print(unique_nfts_link)
        create_data(transactions_link, unique_nfts_link, value)

# value = '0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6'
# transactions_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/historical/past_' + value + '.csv'
# unique_nfts_link = str(pathlib.Path(__file__).parent.resolve()) + '/data/transactions/all_' + value + '.csv'
# clean_null_data_transactions_data(transactions_link, value)
# print(transactions_link)
# print(unique_nfts_link)
# create_data(transactions_link, unique_nfts_link, value)    


# transactions_link = '/home/apb121/csv_files/0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B.csv'
# unique_nfts_link = '/home/apb121/all_0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B.csv'




# headers = ['body','hats','shirt','face','tier','numberOfTraits', 'blockNumber','timestamp']
