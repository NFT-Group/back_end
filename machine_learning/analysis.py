import numpy as np
from sklearn import metrics

def analyse_results(y_pred, y_test, name):
        print('Collection: ' + name)
        print('MAE:' , metrics.mean_absolute_error(y_test, y_pred))
        print('MSE:', metrics.mean_squared_error(y_test, y_pred))

        # note this is returned as a percentage out of 100 and not out of 1
        # having the number of trees = 32 makes for faster model rendering 
        # but we greatly increase the MAPE scores (especially of boredapekennel)
        # by increasing it to 128 trees
        print('MAPE:', metrics.mean_absolute_percentage_error(y_test, y_pred))

        # the point of this is to help explain the potential large MAPEs on
        # certain run throughs of the analysis. We think this could be related 
        # to a few massive anomalies skewing the data and this could prove it
        print("Max Error: ", metrics.max_error(y_test, y_pred))

        # for positive results coefficient of variation is a good measure to compare different models
        # print('Coefficient of variation: ', metrics.mean_squared_error/metrics.mean)