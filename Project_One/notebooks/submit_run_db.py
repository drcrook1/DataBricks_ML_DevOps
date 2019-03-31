import os
import azureml.core
from azureml.core.runconfig import JarLibrary
from azureml.core.compute import ComputeTarget, DatabricksCompute
from azureml.exceptions import ComputeTargetException
from azureml.core import Workspace, Experiment
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import DatabricksStep
from azureml.core.datastore import Datastore
from azureml.data.data_reference import DataReference
from azureml.core.conda_dependencies import CondaDependencies
import ast

def resolve_dependencies():
    """
    ENV VAR OF FORM: "['numpy', 'scikit-learn', 'azureml-sdk']"
    """
    dep_list = ast.literal_eval(os.environ["DEP_LIST"])
    return dep_list

def resolve_compute_name():
    return os.environ["COMPUTE_NAME"]

def resolve_rg():
    return os.environ["RESOURCE_GROUP"]

def resolve_db_workspace_name():
    return os.environ["DB_WORKSPACE_NAME"]

def resolve_db_access_token():
    return os.environ["DB_ACCESS_TOKEN"]

def resolve_script_name():
    return os.environ["SCRIPT_NAME"]

def resolve_subscription_id():
    return os.environ["SUBSCRIPTION_ID"]

def resolve_ml_workspace_name():
    return os.environ["ML_WORKSPACE_NAME"]

def resolve_source_directory():
    return os.environ["SOURCE_DIR"]

def resolve_db_cluster_id():
    return os.environ["DB_CLUSTER_ID"]

my_env = CondaDependencies.create(conda_packages=resolve_dependencies())

with open("myenv.yml","w") as f:
     f.write(my_env.serialize_to_string())


ws = Workspace(resolve_subscription_id(), resolve_rg(), resolve_ml_workspace_name())


config = DatabricksCompute.attach_configuration(
        resource_group = resolve_rg(),
        workspace_name = resolve_db_workspace_name(),
        access_token = resolve_db_access_token())
databricks_compute=ComputeTarget.attach(ws, resolve_compute_name(), config)
databricks_compute.wait_for_completion(True)

dbPythonInLocalMachineStep = DatabricksStep(
    name="DBPythonInLocalMachine",
    python_script_name=resolve_script_name(),
    source_directory=resolve_source_directory(),
    run_name='DB_Worst_Regression_Run',
    compute_target=databricks_compute,
    existing_cluster_id=resolve_db_cluster_id(),
    allow_reuse=True
)


steps = [dbPythonInLocalMachineStep]
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline_run = Experiment(ws, 'DB_Python_Local_demo').submit(pipeline)
pipeline_run.wait_for_completion()


#from azureml.widgets import RunDetails
#RunDetails(pipeline_run).show()