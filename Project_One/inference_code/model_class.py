"""
@Description: Model wrapper class for testability.
@Author: David Crook
@Author_Email: DaCrook@Microsoft.com

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
import pickle
import sys
sys.path.append("../azureml-app/") 
from inference_code.utility import transform_input

class MyModel:
    x_scaler = None
    y_scaler = None
    model = None

    def init(self):
        root_path = "./assets/"
        with open(root_path + "x_scaler.pkl", "rb") as xfile:
            self.x_scaler = pickle.load(xfile)
        with open(root_path + "y_scaler.pkl", "rb") as yfile:
            self.y_scaler = pickle.load(yfile)
        with open(root_path + "model.pkl", "rb") as mfile:
            self.model = pickle.load(mfile)

    def predict(self, input_package):
        """
        input_package: json formatted string of the form
        {"age": integer, "hours-per-week" : double, "sex" : string, "occupation" string}

        returns json formatted string of the form: {"estimated_wages" : float}
        """
        x = transform_input(input_package)
        x = self.x_scaler.transform(x)
        y = self.model.predict(x)
        y = self.y_scaler.inverse_transform(y)
        return y