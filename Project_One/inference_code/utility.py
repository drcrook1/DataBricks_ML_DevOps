"""
@Description: Utility class for transformation of the data package
@Author: David Crook
@Author_Email: DaCrook@Microsoft.com

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
import json
import numpy as np

def transform_input(input_package):
    """
    input_package: raw json input package as agreed upon
    returns: numpy array of correct format without pre-processing
    """
    d = json.loads(input_package)
    # Add extra processing for some reason.
    x = np.array([d["age"], d["hours-per-week"]]).transpose()
    return x

def transform_output(y):
    """
    takes raw output from model and transforms it into the agreed upon interface for worldly consumption
    """
    d = {"estimated_wages" : y}
    return json.dumps(d)