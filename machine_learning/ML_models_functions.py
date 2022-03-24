from sklearn.ensemble import RandomForestRegressor
import math
from sklearn.metrics import mean_squared_error


def random_forest_reg(x_train, x_test, y_train, y_test):
        train_error=[]
        test_error=[]
        minDepth=20
        maxDepth=40
        models=[]
        regr=RandomForestRegressor(max_depth=maxDepth, random_state=0,n_estimators=32)
        regr.fit(x_train, y_train)
        # for depth in range(minDepth,maxDepth,5):
        #         models.append(regr)
        #         tr_error=math.sqrt(mean_squared_error(regr.predict(x_train),y_train))
        #         te_error=math.sqrt(mean_squared_error(regr.predict(x_test),y_test))
        #         test_error.append(tr_error)
        #         train_error.append(te_error)

        y_pred = regr.predict(x_test)
        return(y_pred, y_test, regr)
