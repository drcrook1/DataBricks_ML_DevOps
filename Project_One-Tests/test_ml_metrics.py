import sys
import os
import pytest
sys.path.append("../azureml-app/") #append path for 1 module level up.
from inference_code.model_class import MyModel
from sklearn.metrics.regression import r2_score


class Super_secret_data:
    [x] = {""}
    [y] = {""}

class TestMLMetrics(object):
    """
    testing of the model
    """
    def setUp(self):
        pass

    def test_r2_within_business_value(self):
        m = MyModel()
        print("initing Model")
        m.init()
        
        # Add code to load your super secret cross validation stuff
        # use secrets encoded in a variable group available in the ADO Pipeline
        # cuz scientists can't access that and game the system.

        x1 = '{"age": 37, "hours-per-week": 40.0, "sex": "Female", "occupation" : "Exec-managerial"}'
        y1 = [200000, 190000]
        # We will now make the prediction and since we have a single sample, will create 2 points by adding and subtracting 10
        # just for creating passable data to r2_score - note that this is a meamingless exercise just to demonsrtate the process
        # In real case, you will have more meaningful tests and asserts
        
        y_predicted = m.predict(x1)[0][0]
        ypred = [y_predicted+10, y_predicted-10]
        print (ypred)
        r2score = r2_score(y1, ypred)
        
        assert(-2 < r2score < 2 )

        
