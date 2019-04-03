import sys
import os
import pytest
sys.path.append("../azureml-app/") #append path for 1 module level up.
from inference_code.model_class import MyModel
from sklearn.metrics.regression import r2_score

class TestMLMetrics(object):
    """
    testing of the model
    """
    def setUp(self):
        pass

    def test_r2_within_business_value(self):
        m = MyModel()
        m.init()
        
        # Add code to load your super secret cross validation stuff
        # use secrets encoded in a variable group available in the ADO Pipeline
        # cuz scientists can't access that and game the system.
        super_secret_data = None

        y_predicted = m.predict(super_secret_data[x])
        
        r2_score(super_secret_data[y], y_predicted)

        assert(r2_score > 2 < r2_score)
        
