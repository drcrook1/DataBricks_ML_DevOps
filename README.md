# Data Bricks HOL  - Python & Dev Ops

## Hands on Lab – Abstract
This hands on lab is designed for the scenario where a team of scientists and engineers are responsible for the development, maintenance and quality of analytical models which are made available to other teams for consumption.
## Infrastructure Set Up
This section covers all infrastructure between Azure Dev Ops and Azure resources for the HOL which must be completed prior to the lab.
## Azure Resource Creation
Covers the creation of all required Azure resources.
Create Resource Groups
Begin by creating 3 resource groups.
*	[some-name]-db-dev
*	[some-name]-db-pipeline
*	[some-name]-db-prod

    ![alt text](./readme_images/add_resource_groups.png)

### **Adding Resources to Resource Groups**
These steps should be completed for resource groups [some-name]-db-dev and [some-name]-db-pipeline.  
[some-name]-db-prod will have different resources completely.

---
#### *Add Machine Learning Service Workspace*
1.	Select “Add a Resource”.

    ![alt text](./readme_images/add_resource.png)

2.	Search for “machine learning” and select “Machine Learning service workspace” published by Microsoft.  Click Create

    ![alt text](./readme_images/add_ml_workspace.png)

3.	Populate the fields with a naming convention that makes sense to you.  Select the correct resource group and ensure the location pairs with your other services.

    ![alt text](./readme_images/populate_ml_workspace_resource_creation_settings.png)

---
#### *Add Data Lake (Azure Storage gen 2)*
1.	Select “Add a Resource” form within a resource group pane.

    ![alt text](./readme_images/add_resource.png)

2.	Search for “Storage” and select “Storage account” and click “create”

    ![alt text](./readme_images/select_storage_account.png)

3.	Fill out the creation form.  Ensure you are in the correct resource group.  Give the account a name, ensure it is StorageV2 and set access tier to Cool.

    ![alt text](./readme_images/adls_gen2_basic_settings.png)

4.	Click on “Advanced” and ensure “Hierarchical namespace” under “Data Lake Storage Gen2” is selected as “enabled”.

    ![alt text](./readme_images/adls_gen2_advanced_settings.png)

5.	Select Create
---
#### *Add Azure Key Vault*
1.	Select “Add a Resource” from within a resource group pane.

    ![alt text](./readme_images/add_resource.png)

2.	Search for “key vault” and select “Key Vault” published by Microsoft.

    ![alt text](./readme_images/add_keyvault.png)

3.	Populate the creation form.  Give a name that is easy to remember and ensure the resource group is the desired resource group as well as the location.

    ![alt text](./readme_images/key_vault_creation_form.png)

---
#### *Add a DataBricks Cluster*
1.	Select “Add a Resource” from within a resource group pane.

    ![alt text](./readme_images/add_resource.png)

2.	Search for DataBricks and select the one published by Microsoft.  Click “create”.

    ![alt text](./readme_images/add_adb.png)

3.	Complete the Form for Creation using [some-name] as the workspace name, the resource group you are operating in for the resource group, select a location and ensure pricing tier is “Premium”.  We will be using RBAC controls.  

    ![alt text](./readme_images/adb_creation_form.png)

4.	Navigate back to your resource group and select your newly created workspace

    ![alt text](./readme_images/select_adb_from_rg.png)

5.	Select to “Launch Workspace” – Do not use the URL link. In the top right.

    ![alt text](./readme_images/launch_adb_workspace.png)

6.	On the left hand pane, select “Clusters” and then “Create Cluster”

    ![alt text](./readme_images/create_adb_cluster.png)

7.	Fill out the creation form.  MAKE SURE you select “terminate after 120 minutes of inactivity” to help reduce accidental usage and billing.

    ![alt text](./readme_images/adb_cluster_creation_form.png)

#### *Add AzureML SDK as Library to Cluster.*
1.	From the DataBricks Workspace, click on “Clusters” and then the cluster name.

    ![alt text](./readme_images/select_cluster_for_configure.png)

2.	Click on the Libraries Tab, Install New, PyPl and enter “azureml-sdk”.  Click Install

    ![alt text](./readme_images/add_azml_sdk_to_cluster.png)

---
#### *Add Initial Data to Storage*
We want to ensure there is some data in the various data lakes so folks can access it.
1.	Download the file: https://amldockerdatasets.azureedge.net/AdultCensusIncome.csv 
2.	Select the storage v2 from your resource group.

    ![alt text](./readme_images/select_storage_gen2.png)

3.	Select File Systems from the pane on the left and click "+ File system"

    ![alt text](./readme_images/adls_add_filesystem.png)


4.	Name the file system "datalake"
5.  Click on the newly created "datalake" file system

    ![alt text](./readme_images/adls_select_filesystem.png)

6.  Select "Download Azure Storage Explorer" if you do not already have it installed.
7.  Once Azure Storage Explorer is installed, open it.  Add an Account and Login using your Azure credentials.

    ![alt text](./readme_images/storage_explorer_add_account.png)

8.  Find your filesystem inside the account you have now added.  Drag and drop the AdultCensusIncome.csv into the main pane.  Click Refresh if it does not refresh automatically.

    ![alt text](./readme_images/storage_explorer_add_data.png)

---
#### *Create Secrets for Secure & Controlled Storage Mounts*
We parameterize out a few extra values such that the code for mounting data can remain the same regardless of which databricks cluster it is attached to and the access to data is controlled by a cluster & data lake admin instead.  These steps should be completed for each databricks workspace within each resource group.
##### Install Azure & Data Bricks CLI
1.	Ensure python 3.x is installed.
a.	If it is not; the easiest way is to install Anaconda.
b.	https://www.anaconda.com/download/ 
2.	Install the data bricks cli
a.	Open a cmd prompt and execute the command: “pip install databricks-cli”
3.	Install the azure cli
a.	Open a cmd prompt and execute the command: “pip install azure-cli”
##### Configure Data Bricks CLI for User
>###### Generate a User Access Token
1.	Launch the DataBricks Workspace from the Azure Portal

    ![alt text](./readme_images/launch_adb_workspace.png)

2.	In the upper right hand side of the screen, select the user icon.

    ![alt text](./readme_images/select_adb_user_icon.png)

3.	Select “User Settings” from the drop down.
4.	Select “Generate a New Token”

    ![alt text](./readme_images/generate_adb_token.png)

5.	Give a good comment and remove the token lifetime (gives permanent token access to cluster; not a best practice)

    ![alt text](./readme_images/adb_token_life.png)

6.	Copy the token that gets generated.
>###### Authenticate CLI with Token using Profiles
1.	Use the command “databricks configure --token --profile [PROFILENAME]
a.	HINT: use dev, test & prod similar to how you named the workspaces and resources groups to more easily differentiate.
2.	Enter the host URL
a.	https://eastus.azuredatabricks.net (example)
b.	Paste the token generated from the previous step
3.	To use the profiles capability; simply use the –profile flag with the [PROFILENAME] configured to configure the workspace you are targeting.
>###### Create Service Principal and Give Access to Data Lake
This section uses an AD Service principal and provides access to the principal for the data.
1.	Login in to the azure cli by executing the command: “az login”
a.	Follow instructions printed out.
2.	Create a service principal by executing the command: “az ad sp create-for-rbac –name [SOMENAME]”
a.	Copy the app id
b.	COPY the password – you will not be able to get it again.
3.	Get the Service Principal’s object id by executing the command: “az ad sp show –id [AppId]”.  Search through the result and find the value of the property “objectId”
b.	Copy the objectID

    ![alt text](./readme_images/copy_sp_obj_id.png)

4.	Open Azure Storage Explorer and right click the datalake container you created previously.  Select “Manage Access”

    ![alt text](./readme_images/manage_dl_access.png)

5.	Paste the objectID into the text box and click “Add”

    ![alt text](./readme_images/paste_obj_id_as_user_to_dl.png)

6.	Find the object ID in the list, click on it and give it Read, Write & Execute Access as well as Default.  Click Save

    ![alt text](./readme_images/grant_sp_dl_access.png)

7.	Navigate to the Azure Portal and to the ADLS Gen Two Blade for this resource group.  Click on Access Control (IAM)

    ![alt text](./readme_images/acccess_control_pane_adls_gen2.png)

8.	Click on “Add” “Add role assignment”

    ![alt text](./readme_images/add_role_adls_gen2.png)

9.	The role should be: “Storage Blob Data Contributor” and enter the name for the service principal for this resource group you created and click save.

    ![alt text](./readme_images/adls_gen2_role_add_form.png)

>###### Create an Azure Key Vault Backed Secret Scope
1.	Navigate to your Databricks workspace (create Secret Scope) with the following format:
* a. 	https://eastus.azuredatabricks.net/?o=6776691945951303#secrets/createScope 
* b.	Replace the number after o= with yours:

     ![alt text](./readme_images/get_adb_workspace_id.png)

* c.	Or simply append #secrets/createScope to the end of the url of your workspace.
2.	**Now Navigate to the key vault** for the resource group you are setting up:

    ![alt text](./readme_images/navigate_key_vault.png)

3.	Copy the DNS name

    ![alt text](./readme_images/copy_kv_dns_name.png)

4.	Copy the Resource ID

    ![alt text](./readme_images/copy_kv_resource_id.png)

5.	**Navigate back to Databricks workspace (create Secert Scope)** and name the scope “data-lake”, set for “All Users”.  Populate the dns name and resource id of the key vault. And select “Create".

    ![alt text](./readme_images/adb_create_secret_scope.png)

6.	From the databricks CLI, enter the command: “databricks secrets list-scopes –profile [YOUR PROFILE]

    ![alt text](./readme_images/confirm_kv_backed_secret_scope.png)

>###### Add Secrets to Secret Scope for Accessing Data
You will need the Service Principal’s password and app id from the previous steps.
1.	Get the app’s tenant id by executing the following command: “az ad sp show –id [AppId]”
a.	Copy the value from: “appOwnerTenantId”.
2.	Add the Service Principal’s TenantID to the Azure Key Vault
a.	“az keyvault secret set –vault-name [KeyVault for RG] –name “sp-tenant-id” –value [TenantId]”
3.	Add the Service Principal App-ID to the Azure Key Vault
a.	“az keyvault secret set –vault-name [KeyVault for RG you are configuring] –name “sp-app-id” –value [service principal’s app id]

    ![alt text](./readme_images/kv_add_sp_app_id_secret.png)

4.	Add the Service Principal’s password to the Azure Key Vault
a.	“az keyvault secret set –vault-name [KeyVault for RG] –name “sp-password” –value [password copied from earlier]
5.	Add the Service Principal’s token endpoint
a.	https://login.microsoftonline.com/YOURAPPOWNERTENANTID/oauth2/token
b.	“az keyvault secret set –vault-name [KeyVault for RG] –name “sp-token-endpoint” –value [token endpoint]
6.	Add the FQDN of the data lake.
a.	“az keyvault secret set –vault-name [KeyVault for RG] –name “datalake-fqdn” –value “abfss://datalake@YOURSTORAGEACCOUNT.dfs.core.windows.net”
7.  Add the subscription id for the ml service.  Navigate to the ml service inside your resource group and copy the subscription id.
    1.  "az keyvault secret set --vault-name [KeyVault for RG] --name subscription-id --value YOURSUBSCRIPTIONID

    ![alt text](./readme_images/mlservice_subscription_id.png)

8.  Add the resource group for the ml service.  Navigate to the ml service inside your resource group and copy the resource group id.
    1.  "az keyvault secret set --vault-name [KeyVault for RG] --name resource-group --value YOURRGNAME

    ![alt text](./readme_images/mlservice_rg_name.png)

9.  Add the ml service workspace name.  Navigate to the ml service within the appropriate resource group and copy the name.
    1.  "az keyvault secret set --vault-name [KeyVault for RG] --name ml-workspace-name --value YOURVALUE

    ![alt text](./readme_images/mlservice_name.png)

10.  Add the "Alg State"  This changes per resource group.  For the Dev RG, it is "dev", for "Pipeline" it is "pipeline".  If you were to add additional clusters for releases for multi-tenancy it should have a convention to help support that.
     1.   "az keyvault secret set --vault-name [KeyVault for RG] --name alg-state --value APPROPRIATEVALUE

11.  Add the "Created By".  For now this will simply match "Alg State"'s conventions.
     1.   "az keyvault secret set --vault-name [KeyVault for RG] --name created-by --value APPROPRIATEVALUE

7.	Verify secrets are in the data-lake scope for databricks
a.	“databricks secrets list –scope data-lake”

## Azure Dev Ops 

Azure Dev Ops is a fully integrated Dev Ops tool with work item features, version control, build and release.  It can also be used to stitch together a variety of other tools into one central dev ops plane.

### **Creation** 

This section covers creating a project in Azure Dev Ops for the workshop.

1.	Navigate to https://dev.azure.com 
2.	Select the organization you intend to use OR create a new organization.
3.	Create a new project.  Pick a name, description.  Select “Git” for version control and “Agile” for the work item process.

    ![alt text](./readme_images/create_ado_project.png)

4.	Invite Additional Users

    ![alt text](./readme_images/add_ado_user_1.png)

    ![alt text](./readme_images/add_ado_user_2.png)

5.	Click on Repos, Files.
6.	At the very bottom, select “Initialize Repo”.

### **Seed the Repo**

We are going to seed your newly created repository with this repository to reduce mistakes during the workshop as well as be able to focus on what everything is doing as opposed to copy/pasting.  This activity should be done only once per new repo.

1.  navigate to https://github.com/drcrook1/DataBricks_ML_DevOps click "Clone or download" and then "Download ZIP"

    ![alt text](./readme_images/download_repo_as_zip.png)

**This will have downloaded to your default "downloads" location. 

2.  Create a new empty folder to hold your projects or navigate to the one you usually use.  I personally use "C:/projects".
3.  Copy the git url for your ADO repository

    ![alt text](./readme_images/copy_clone_git_repo_link.png)

**Note, that you may have to "Generate Git credentials" if you have not done so before.

4.  Navigate to your normal projects folder (C:/projects for me) and execute the command: "git clone PASTEURL"
    1.  This will generate a new folder in it.  The name will be http friendly with special characters (feel free to remove those)

5.  Extract the zip file you downloaded earlier.  Copy all files *except* the .git folder

    ![alt text](./readme_images/not_this_folder.png)

6.  your folder structure should be similar to this:

  FOLDER STRUCTURE

    - C:/projects/
        - YOUR REPO NAME /
          - Project_One/
          - Project_One-Tests/
          - readme_images/
          - .git/ (not extracted one)
          - .pptx (possibly a few)
          - .gitignore
          - README.md

7.  Open a command prompt and use "cd" to change into the your projects repo.  For me the command would be: "cd C:/projects/YOUR_REPO_NAME"
8.  Execute the cmd "git add ./"
9.  Execute the cmd "git commit -m "initial repo seed""
10. Execute the cmd "git push"
11. Your remote repository should now be seeded with the workshop content.

### **Scientists – Initial Setup**
Configure Azure Dev Ops Integrations
 Azure Databricks, set your Git provider to Azure DevOps Services on the User Settings page:
1.	Click the User icon   at the top right of your screen and select User Settings.

    ![alt text](./readme_images/adb_user_settings.png)

2.	Click the Git Integration tab.
3.	Change your provider to Azure DevOps Services.

    ![alt text](./readme_images/ado_git_provider_adb.png)

#### Create & Link Project File w/ Repo
1.	From inside the Data Bricks cluster interface, select workspace, shared, then the drop down, then create and create a “Folder”

    ![alt text](./readme_images/adb_create_folder.png)

2.	Name the folder “Project_One”
3.	Create a new file inside the project called “train_model”.

    ![alt text](./readme_images/adb_create_notebook.png)

4.	Link “train_model.py” file to your Azure Dev Ops repository.
a.	Copy the git link from your azure dev ops portal:

    b.  The format of the link will be: https://dev.azure.com/{yourOrg}/{yourproject}/_git/{yourRepository}

      ![alt text](./readme_images/copy_ado_git_link.png)

b.	Paste into the “link” location in the popup for “Git Preferences”
c.	Create a new branch.  Name it your unique user ID
d.	Use “Project_One/notebooks/train_model.py” as the path in git repo.

   ![alt text](./readme_images/adb_git_link_settings_form.png)

5.  Notice that the latest version appears to have imported everything and then deleted it.  Revert back to the previous commit.  Click on the previous commit and then "Restore this revision".

     ![alt text](./readme_images/restore_original_commit.png)

## Dev Loop Experience
The dev loop experience encompasses mounting the dev data, exploring that data, training a model; writing the inference code, compiling a dev container; running tests inside the dev container.
### **Train the world’s worst regression & Stage for inference coding.**
1.	Copy the code from Project_One/notebooks/train_model.py into your databricks train_model.py which was created earlier.
2.  The proctor will step through what exactly the code is doing and why.
    1.  Essentially: The precreated secrets are being used to mount to various stores securely and will allow zero code changes as the algorithm progresses across secure environments.  
    2.  You train a super simple algorithm and register the resulting model files with the AZML service such that we can bridge the divide between databricks and inference coding.  This process is ML Framework independent and can be used cross algorithms, frameworks etc.

**Note:** that when you run the code/cell, it will require you to login using your Azure credentials at https://microsoft.com/devicelogin. Unless you perform this step external to Databricks, the run will not complete.
### **Inference Coding**
This section extends from having a trained model to now building an inference container which is reflective of the asset we will deliver to our customer base.

>Code Structure

  ![alt text](./readme_images/inference_code_structure.png)

Good Code Structure from the beginning is a great way to ensure you are set up well.  In this case we are going to follow well defined development strategies via a bit of a hybrid between .net project structures and python project structures.
 
We have two folders for each project.  Project_One is the primary inference project
### **Git Pull the train code**
1.	Open a cmd prompt.
2.	Change directory into the root of where your project is.
3.	Execute the commands:
```   
   a.	“git checkout <YOURBRANCHNAME>”
   b.	“git pull”
```
### **Test Driven Development**

#### Write a Test
You should always start with testing and then writing code to satisfy those tests.  The only code which will be required to write is the test_model.py.  The facilitation code here is provided for you.

   ![alt text](./readme_images/test_model_view.png)
 
Inside this file we will write a very simple unit test to ensure that the x_scaler object is populated during model initialization.

1.  An example unit test has already been written.  Add 1 more unit test to Project_One-Tests/test_model.py.
2.  The facilitation code follows standard pytest rules, so you can even add more test files etc; just follow pytest conventions.
3.  The proctor will run through how the project works.
    1.  Project_One is the project code which seperates the inference code as a "provider" type class following similiar principals from the testable web dev space.  
    2.  Project_One-Tests is your seperated testing code such that it is not coupled with your app development code.
    3.  A container is built for the inference code, which is then extended with the test code.  The base inference container is the asset expected to be deployed while the extended testing container allows you to test the assets in the same type of format as if they were to be compiled.

#### Review Inference Code
Normally we would test and ensure the tests fail before writing the inference code; however much of the code is already written, so we will simply review it.

   ![alt text](./readme_images/inference_code_review.png)

In an ideal world, the only code you would need to worry about is highlighted in red.  The current state of tooling as of today is why the other code exists and is not wrapped up as ADO Tasks or VS Code extensions.  

The proctor will run through the code with your, but essentially:
1.  ./Project_One/score.py is what the azure ml sdk expects as the interface and must be populated with an init() and a run(params).  The params are what is received in the http request body (or iot edge message over the route)
2.  The code placed in inference_code is to help ensure code coverage is reported appropriately.  We follow a similar provider type structure as in web dev when there is a pre-defined functional interface.  The objective is to minimize that footprint to 1 line of code. (in score.py init and run)
3.  The rest of the code is a dockerized build process that can run independent of the dependencies installed on your system such that the build on your machine is the same as the build in the build server improving confidence the locally generated and tested asset will match the asset which has probability of being promoted to production.

We now have inference code with matching train code.  Lets build the inference container and test it.
### **Build Inference Container**
1.	First open runbuild_local.cmd
a.	Modify the environment variables to match for the dev environment.  These will remain constant for this algorithm and your local environment.
i.	Subscription_id
ii.	Ml_resource_group
iii.	Ml_workspace_name
iv.	Ml_alg_author
From the command prompt:
1.	Change directory into the Project_One folder.
2.	Run the runbuild_local.cmd
a.	You may need to execute az login prior to executing this command or be interactively logged in (watch the output)

    ![alt text](./readme_images/run_build_local.png)
>Note: you may need to login for Azure ACR using: az acr login --name [acrName]
you can find the acrName in the dockerfile FROM statement in the Project_One-Tests folder

c.	This will execute a bunch of stuff and be on “Creating image” for a while.  Occasionally hit enter to see if the cmd prompt output is up to date or not.

   ![alt text](./readme_images/successful_local_build.png)

### **Test Inference Container**
1.	Change directory into the Project_One-Tests folder.
2.	Run the runtests_local.cmd file
>Note: Make sure that you have access to Azure ACR by running command: docker login -u [Username] -p [password] loginServerName
you can find the loginServerName, Username and password on the Access keys tab of the ACR in Azure Portal   
3.	This will extend the container you created in the previous step, run your unit tests and check your code coverage.  The code coverage results can be found in C:/ml_temp/artifacts/test_results  These are standard pytest and pytest-cov result outputs.

    ![alt text](./readme_images/test_results.png)

5.	Click on index.html from cov_html folder

    ![alt text](./readme_images/local_test_results_web.png)

7.	We have 68% code coverage; could be worse.
### **Commit & Pull Request.**
1.	We now know that we have an inference container and it passes our unit tests and our code coverage is to a point where we are happy about it.
2.	From the command prompt change directory to the root of the repository.
3.	Execute the following commands to push the changes from your branch:
a.	Git add ./
b.	Git commit -m “works”
c.	Git push
4.	Create a pull request by going to your ADO site, under repos, pull request, New Pull Request

    ![alt text](./readme_images/create_pull_request.png)

5.	Populate the request template and ensure you have a reviewer:

    ![alt text](./readme_images/PR_options_form.png)

6.	Review the changes with the reviewer you selected.  Ensure both enter ADO and hit “Approve” and then “Complete”.  If you see problems in your peers code; add comments and reject it.  Once both reviewers Approve you can complete.  This will launch the build pipelines & release pipelines which are connected to master.
 
---
## Defining your Build Pipeline

Since we are targeting a different Azure Databricks Environment than the one used in the local Dev Loop described earlier in this document, and since we are concerned with security we will be creating a library asset which will allow us to define secrets from a key vault that points to this new environment. These secrets become available as variables in the build pipeline. Variables give you a convenient way to get key bits of data into various parts of the pipeline. As the name suggests, the value of a variable may change from run to run or job to job of your pipeline. Almost any place where a pipeline requires a text string or a number, you can use a variable instead of hard-coding a value. The system will replace the variable with its current value during the pipeline's execution.
### **Confirm Secrets Availability**
In addition to the secrets used in the previous sections, the following secrets must be available in the KeyVault associated with the Resource Group for the Build Pipeline to work properly:
* compute-name
* db-workspace-name
* db-access-token
* db-cluster-id
* model-name
* image-name
  
>Note: To get db-cluster-id, after creating the cluster in Databricks, select the cluster then 'Advanced Options' and navigate to the 'Tags' tab.
  
   ![alt text](./readme_images/ado_build_cluster_id.png)

### **Creating a Variable Group**

1.	In your Azure DevOps Subscription navigate to the Library Menu Item and click + Variable Group

    ![alt text](./readme_images/create_variable_group_ado.png)

2.	Name your variable group as indicated and select the Azure Subscription and KeyVault that you wish to target and toggle the “Link secrets from an Azure key vault as variables” switch to the on position
 
     ![alt text](./readme_images/ado_variable_group_form.png)

3.	Click the + Add button, select the variables that you want to make available to the pipeline, click ok and then Save to make sure that your changes are persisted to your Azure DevOps instance
 
    ![alt text](./readme_images/ado_variable_group_available_to_pipeline.png)

### **Create a Build Pipeline in the Visual Designer**

The intention of this step is to create an Azure DevOps Pipeline that will mimic the steps from the Local Build Loop, but targets a different Azure Databrick Environment for the training .The connection details of this environment will not be available to the scientists directly and will be managed by the operations team. This pipeline will execute when a PR to master is approved and completed.
>Note: On top-right select your initials or picture and then select 'preview features' and turn off 'New YAML pipeline creation experience' if not already off

1.	In your Azure DevOps tenant, navigate to Pipelines -> Builds and click on + New and select New build pipeline.
 
    ![alt text](./readme_images/ado_new_build_pipeline.png)

2.	Select your source and make sure to select the master branch as we want to make sure that the pipeline is attached the branch that we will be monitoring for Pull Requests. Click Continue.

    ![alt text](./readme_images/ado_build_pipe_repo_type.png)

3.	Select Empty Job 

    ![alt text](./readme_images/ado_build_pipe_select_empty_job.png)

4.	Name your Pipeline accordingly and select the Hosted Ubuntu 1604 Build Agent from the Agent Pool.

    ![alt text](./readme_images/ado_build_pipe_set_build_agent_type.png)

5.	Link the variable group that you created earlier by clicking on Variables in the menu bar, followed by Variable groups and click Link Variable Groups.

    ![alt text](./readme_images/ado_build_pipe_link_variable_group.png)
 
6.	Select the Staging Environment Variable Group and Click Link. Your pipeline now has access to all the runtime environmental variables to connect to the Staging Environment.

    ![alt text](./readme_images/ado_build_pipe_var_group_staging.png)

7.	Click back onto Tasks on the menu and click +on the Agent Job to Add the Tasks that you will be configuring for the build process.

    ![alt text](./readme_images/ado_build_pipe_staging_add_tasks.png)
 
8.	Type “CLI” in the Search Box and Click the Azure CLI”ADD” button four times.

    ![alt text](./readme_images/ado_build_pipe_add_cli_tasks.png)

Your Agent Job Step should look like the following when you have completed.

![alt text](./readme_images/four_empty_cli_tasks.png)
 

1. Repeat Step 8 above, but instead of “Azure CLI” add two "Copy Files" Tasks. 

  ![alt text](./readme_images/copy_files_task.png)

10.	Similarly, add a "Publish Test Results" Task
 
   ![alt text](./readme_images/publish_test_results_task.png)


11.	Finally, add a "Publish Code Coverage Results" Task.

     ![alt text](./readme_images/pub_code_coverage.png)
 
 Your Agent Job should now resemble the following:

   ![alt text](./readme_images/verify_ado_build_pipe_post_pub_cov_add.png)

12.	The First Azure CLI Task will be used to configure the agent environment and make sure that the required packages are installed to execute the rest of the pipeline. Provide the task with a descriptive name, Select the appropriate Azure Subscription, set the Script Location to “Inline Script” and add the flowing to the inline script window:
      * pip3 install -U setuptools
      * python3 -m install --upgrade pip
      * pip3 install --upgrade azureml-sdk[notebooks]

Set the remainder of the task properties as depicted below:
 
![alt text](./readme_images/ado_cli_task_1.png)

![alt text](./readme_images/ado_cli_task_1_vars.png)

13.	Click on the second Azure CLI Task, select the appropriate Azure Subscription and configure as follows:

    ![alt text](./readme_images/ado_cli_task_2_config.png)

14.	Click in the third Azure CLI Task , select the appropriate Azure Subscription and configure the Task as follows :

    ![alt text](./readme_images/ado_cli_task_3_config.png)

    ![alt text](./readme_images/ado_cli_task_3_config_p2.png)

15.	Click the fourth Azure CLI Task, Select the appropriate Azure Subscription and configure the Task as follows:

    ![alt text](./readme_images/ado_cli_task_4_config_p1.png)

    ![alt text](./readme_images/ado_cli_task_4_config_p2.png)

16.	Click on the first Copy Files Task and configure the task as follows:

    ![alt text](./readme_images/ado_copy_files_1.png)

    ![alt text](./readme_images/ado_copy_files_1_p2.png)

17.	Click on the second Copy Files Task and configure the task as follows:

    ![alt text](./readme_images/ado_copy_files_3_p1.png)

    ![alt text](./readme_images/ado_copy_files_2_p2.png)
 
18.	Click on the Publish Test Results Task and Configure the task as follows:

    ![alt text](./readme_images/ado_pub_test_p1.png)

    ![alt text](./readme_images/ado_pub_test_p2.png)
 
19.	Click on the Publish Code Coverage Task and configure the task as follows:

    ![alt text](./readme_images/ado_pub_test_cov_p1.png)

     ![alt text](./readme_images/ado_pub_test_cov_p2.png)

20.	 On the Agent Job Click the + in order to add a task that will be used to publish the build artifacts for use in a release pipeline later.

     ![alt text](./readme_images/ado_add_task.png)

Search for Publish and Click “Add” on the Publish Build Artifacts Task
 
  ![alt text](./readme_images/ado_add_pub_artifacts.png)

Configure the task as follows:

  ![alt text](./readme_images/ado_add_pub_artifacts_config.png)

  ![alt text](./readme_images/ado_add_pub_artifacts_config_p2.png)
 
21.	Enable the Continuous Integration trigger on the pipeline which will make sure that every time a change in made to the master branch of the repository this pipeline will execute. Click the Triggers menu item in the menu bar and click the checkbox to enable continuous integration.
 
    ![alt text](./readme_images/ado_cont_int_trigger.png)

You can now Save and Queue this pipeline for a manual build to make sure that it executes from end to end without any issues. 

Output from the pipeline should resemble the following:
 
   ![alt text](./readme_images/ado_output_successful_build.png)

---
## Defining your Release Pipeline

While release pipelines are often used to deliver artifacts in a deployed state, our scenario calls for an different approach. Our build artifact is an image that contains our tested model and we will be creating a Two Stage Release that will first deliver the correct image to aQA environment where it can be picked up and be tested by a product team. Once all conditions for the product team is satisfied a release manager will manually approve the Production release step and the model will become available for consumption in the Production Environment.
Creating Variable Groups Required for the Release Pipeline
1.	Click on the Library menu item in the Azure DevOps portal and click 

    ![alt text](./readme_images/ado_rp_add_variable_group.png)

2.	Complete the resulting form as depicted below, making sure that you provide values to the variables that correspond to the Targeted QA Environment

    ![alt text](./readme_images/ado_rp_qa_variable_form.png) 

3.	After each Variable Value has been assigned click the   to encrypt its value in the pipeline.
4.	Repeat Steps 2 and 3 above to set up a variable group for the targeted Production Environment.
### **Create the Release Pipeline**
1.	In the Azure DevOps portal Click on Pipelines -> Releases in the left menu

    ![alt text](./readme_images/ado_rp_rp_button_click.png) 

2.	Click The New pipeline menu item and select New release pipeline 

    ![alt text](./readme_images/ado_rp_new_rp.png) 

3.	Add Two Stages, Named QA and Production Respectively ensuring that you select the “Empty Template”. Click on the Pre-deployment condition icon     and continue to configure as depicted below. This will prevent the Production deployment from happening automatically unless there is an Approval provided by One or all of the Approvers (dependent on configuration) and that the Production Stage Deployment will timeout after two days with out an approval.

    ![alt text](./readme_images/ado_rp_gated_prod.png) 

4.	Add the build artifacts and link the release pipeline to its associated build pipeline.

    ![alt text](./readme_images/ado_rp_add_build_artifacts.png) 

Note: The value  in the Source alias text area will be required to correctly configure the AZ CLI tasks in Steps 6 and 7 below.
 

5.	In the Menu area select variables and link the QA and Production variable to the relevant slots.

    ![alt text](./readme_images/ado_rp_link_variable_groups.png) 

6.	Add a CLI Task to the QA Stage and configure it as follows :

    ![alt text](./readme_images/ado_rp_qa_cli_1.png) 

    ![alt text](./readme_images/ado_rp_qa_cli_2.png) 

** Make sure that the working directory set above reflects the generated path correct path here
$(System.DefaultWorkingDirectory)/<Insert Correct Path Here>/PipelineArtifacts

7.	Repeat Step 6 above for the Production Stage . 

Note that the script internals are identical for both stages but will target different destination repositories based on the Variables groups assigned to each of the stages.

![alt text](./readme_images/ado_rp_prod_cli_reveal.png) 

8.	Run a release and inspect the results
9.	To automate the release process click the Continuous Integration Trigger of the Build Artifact and set as follows.

    ![alt text](./readme_images/ado_rp_automate_rp.png) 

    ![alt text](./readme_images/ado_rp_automate_rp_2.png) 

10.	Finally click on the Pre-Release Condition for the QA Stage    and set as follows.

    ![alt text](./readme_images/ado_rp_qa_prerelease_condition.png) 
 
11.	A successful release will resemble the following
 
    ![alt text](./readme_images/ado_rp_success_1.png)

    ![alt text](./readme_images/ado_rp_success_2.png)
 

