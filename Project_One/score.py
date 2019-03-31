import json
from inference_code.model_class import MyModel

MODEL = None

def init():
    global MODEL
    MODEL = MyModel()
    MODEL.init()

def run(input_package):
    return MODEL.predict(input_package)