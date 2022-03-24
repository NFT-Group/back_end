import numpy as np

def analyse_results(y_pred, y_test, name):
        #MSE
        from sklearn import metrics
        # print("----------" +
        #         list(collection_addresses_dict.keys())[list(collection_addresses_dict.values()).index(name)]
        #         + "----------\n\n")

        print('Collection: ' + name)
        print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        #MAPE
        def mean_absolute_percentage_error(y_test, y_pred):
                y_test = y_test.astype('float')
                y_pred = y_pred.astype('float')
                y_test, y_pred = np.array(y_test), np.array(y_pred)
                return np.mean(np.abs((y_test - y_pred)/y_test)) * 100

        print('MAPE:', mean_absolute_percentage_error(y_test, y_pred))

        # for positive results coefficient of variation is a good measure to compare different models
        # print('Coefficient of variation: ', metrics.mean_squared_error/metrics.mean)