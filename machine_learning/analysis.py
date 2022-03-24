import numpy as np
from sklearn import metrics

def analyse_results(y_pred, y_test, name):
        print('Collection: ' + name)
        print('MAE:' , metrics.mean_absolute_error(y_test, y_pred))
        print('MSE:', metrics.mean_squared_error(y_test, y_pred))
        print('MAPE:', metrics.mean_absolute_percentage_error(y_test, y_pred))

        # for positive results coefficient of variation is a good measure to compare different models
        # print('Coefficient of variation: ', metrics.mean_squared_error/metrics.mean)