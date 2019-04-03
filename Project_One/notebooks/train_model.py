# Databricks notebook source
# FUTURE SERVICE PRINCIPAL STUFF FOR MOUNTING
secrets = {}
secrets["datalake_fqdn"] = dbutils.secrets.get(scope = "data-lake", key = "datalake-fqdn")
secrets["subscription_id"] = dbutils.secrets.get(scope = "data-lake", key = "subscription-id")
secrets["resource_group"] = dbutils.secrets.get(scope = "data-lake", key = "resource-group")
secrets["ml_workspace_name"] = dbutils.secrets.get(scope = "data-lake", key = "ml-workspace-name")
secrets["alg_state"] = dbutils.secrets.get(scope = "data-lake", key = "alg-state")
secrets["sp_app_id"] = dbutils.secrets.get(scope = "data-lake", key = "sp-app-id")
secrets["sp_password"] = dbutils.secrets.get(scope = "data-lake", key = "sp-password")
secrets["sp_tenant_id"] = dbutils.secrets.get(scope = "data-lake", key = "sp-tenant-id")
secrets["sp_token_endpoint"] = dbutils.secrets.get(scope = "data-lake", key = "sp-token-endpoint")
secrets["created_by"] = dbutils.secrets.get(scope = "data-lake", key = "created-by")
if(secrets["created_by"] == "dev"):
  print("dev state, replacing with specific dev alias.")
  secrets["created_by"] = "dacrook"

# COMMAND ----------

#
# THIS IS FOR ADLS V2 Mounting
#
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": secrets["sp_app_id"], #Service Principal App ID
           "fs.azure.account.oauth2.client.secret": secrets["sp_password"], #Service Principal Key
           "fs.azure.account.oauth2.client.endpoint": secrets["sp_token_endpoint"]} #directory id

try:
  #mounting the external blob storage as mount point datalake for data storage.
  dbutils.fs.mount(
    source = secrets["datalake_fqdn"], #blobcontainername@storageaccount
    mount_point = "/mnt/datalake",
    extra_configs = configs)
except Exception as e:
  print("already mounted; no need to do so.")

# COMMAND ----------

#display the files in the folder
dbutils.fs.ls("dbfs:/mnt/datalake")

# COMMAND ----------

census = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('/mnt/datalake/AdultCensusIncome.csv')
census.printSchema()
display(census.select("age", " fnlwgt", " hours-per-week"))

# COMMAND ----------

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

# COMMAND ----------

x = np.array(census.select("age", " hours-per-week").collect()).reshape(-1,2)
y = np.array(census.select(" fnlwgt").collect()).reshape(-1,1)

# COMMAND ----------

x
y

# COMMAND ----------

#Split data & Train Scalers
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state = 777, shuffle = True)
x_scaler = StandardScaler().fit(x_train)
y_scaler = StandardScaler().fit(y_train)

#Transform all data
x_train = x_scaler.transform(x_train)
x_test = x_scaler.transform(x_test)
y_train = y_scaler.transform(y_train)
y_test = y_scaler.transform(y_test)

model = LinearRegression().fit(x_train, y_train)

y_predicted = y_scaler.inverse_transform(model.predict(x_test))

mae = mean_absolute_error(y_test, y_predicted)
r2 = r2_score(y_test, y_predicted)

print(mae)
print(r2)

# COMMAND ----------

#Write Files to local file storage
import os
#Also works: "/dbfs/tmp/models/worst_regression/dacrook/"
prefix = "file:/models/worst_regression/"
if not os.path.exists(prefix):
  os.makedirs(prefix)
with open(prefix + "x_scaler.pkl", "wb") as handle:
  pickle.dump(x_scaler, handle)
with open(prefix + "y_scaler.pkl", "wb") as handle:
  pickle.dump(y_scaler, handle)
with open(prefix + "model.pkl", "wb") as handle:
  pickle.dump(model, handle)
  
#Create an Azure ML Model out of it tagged as dev
from azureml.core.workspace import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model
az_sp = ServicePrincipalAuthentication(secrets["sp_tenant_id"], secrets["sp_app_id"], secrets["sp_password"]) #tenant id
az_ws = Workspace(secrets["subscription_id"], secrets["resource_group"], secrets["ml_workspace_name"], auth= az_sp)
print("Logged in and workspace retreived.")
Model.register(az_ws, model_path = prefix, model_name = "worst_regression", tags={"state" : secrets["alg_state"], "created_by" : secrets["created_by"]})

# COMMAND ----------

#finally unmount the mount.
try:
  dbutils.fs.unmount("/mnt/datalake")
except Exception as e:
  print("already unmounted; no need to unmount again.")
