import sys
import os
import pytest
sys.path.append("../azureml-app/") #append path for 1 module level up.
from inference_code.model_class import MyModel

class TestModel(object):
    """
    testing of the model
    """
    def setUp(self):
        pass

    def test_init(self):
        m = MyModel()
        m.init()
        assert(m.x_scaler is not None)
        assert(m.y_scaler is not None)
        assert(m.model is not None)
        
