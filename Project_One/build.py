from azureml.core.workspace import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model
from azureml.core.image import ContainerImage, Image
from azureml.core.conda_dependencies import CondaDependencies
import os
from os import walk
import shutil
import json

def resolve_sub_id():
    return os.environ["SUBSCRIPTION_ID"]

def resolve_rg():
    return os.environ["RESOURCE_GROUP"]

def resolve_workspace_name():
    return os.environ["WORKSPACE_NAME"]

def resolve_state():
    return os.environ["STATE"]

def resolve_author():
    return os.environ["AUTHOR"]

def resolve_model_name():
    return os.environ["MODEL_NAME"]

def resolve_image_name():
    return os.environ["IMAGE_NAME"]

def run():
    print("entered run")
    variables_received = "sub_id: {}, rg: {}, work_name: {}, state: {}, author: {}, model_name: {}" \
                            .format(resolve_sub_id(),
                                    resolve_rg(),
                                    resolve_workspace_name(),
                                    resolve_state(),
                                    resolve_author(),
                                    resolve_model_name())
    print(variables_received)
                                                                
    az_ws = Workspace(resolve_sub_id(), resolve_rg(), resolve_workspace_name())
    print("initialized workspace")
    #Get & Download model
    model = Model(az_ws, name=resolve_model_name(), tags={"state" : resolve_state(), "created_by" : resolve_author()})
    print("initialized model")
    model.download(target_dir="./assets/")
    print("downloaded model assets")
    #TODO: remove workaround for ml sdk dropping assets into /assets/dacrook folder when files dropped to consistent location
    for dir_p, _, f_n in walk("./assets"):
        for f in f_n:
            abs_path = os.path.abspath(os.path.join(dir_p, f))
            shutil.move(abs_path, "./assets/" + f)

    #Configure Image
    my_env = CondaDependencies.create(conda_packages=["numpy", "scikit-learn"])
    with open("myenv.yml","w") as f:
        f.write(my_env.serialize_to_string())
    image_config = ContainerImage.image_configuration(execution_script = "score.py",
                                                        runtime="python",
                                                        conda_file="myenv.yml",
                                                        dependencies=["assets", "inference_code"],
                                                        tags={"state" : resolve_state(), "created_by" : resolve_author()})
    print("configured image")
    #TODO: use this once model is dropped to a consistent location
#    image = Image.create(workspace = az_ws, name=resolve_image_name(), models=[model], image_config = image_config)
    image = Image.create(workspace = az_ws, name=resolve_image_name(), models=[model], image_config = image_config)
    image.wait_for_creation()
    print("created image")
    if(image.creation_state != "Succeeded"):
        raise Exception("Failed to create image.")
    print("image location: {}".format(image.image_location))
    artifacts = {"image_location" : image.image_location}
    if(not os.path.exists("/artifacts/")):
        os.makedirs("/artifacts/")
    with open("/artifacts/artifacts.json", "w") as outjson:
        json.dump(artifacts, outjson)
    
if __name__ == "__main__":
    run()