# Databricks notebook source
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope = "data-lake", key = "sp-app-id"), #Service Principal App ID
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope = "data-lake", key = "sp-password"), #Service Principal Key
           "fs.azure.account.oauth2.client.endpoint": dbutils.secrets.get(scope = "data-lake", key = "sp-token-endpoint")} #directory id

# Optionally, you can add <your-directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://datalake@dacrookdbdevstorage.dfs.core.windows.net", #blobcontainername@storageaccount
  mount_point = "/mnt/datalake",
  extra_configs = configs)

# COMMAND ----------

census = sqlContext.read.format('csv').options(header='true', inferSchema='true').load("/mnt/datalake/AdultCensusIncome.csv")
display(census)

# COMMAND ----------

#Race condition between display and mounting in interactive environment.
#dbutils.fs.unmount("/mnt/datalake")
