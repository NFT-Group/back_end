from sklearn.ensemble import RandomForestRegressor
import math
from sklearn.metrics import mean_squared_error


def random_forest_reg(x_train, x_test, y_train, y_test):
        train_error=[]
        test_error=[]
        minDepth=20
        maxDepth=40
        models=[]
        # n.b. we want a larger forest than 32 but github doesn't let us use them
        regr=RandomForestRegressor(max_depth=maxDepth, random_state=0,n_estimators=32)
        regr.fit(x_train, y_train)
        y_pred = regr.predict(x_test)
        return(y_pred, y_test, regr)
