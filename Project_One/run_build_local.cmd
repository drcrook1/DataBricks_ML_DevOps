docker stop mlbuild
docker rm mlbuild

if not exist "C:\ml_temp\artifacts" mkdir C:\ml_temp\artifacts

:: REPLACE TOKENS IN dockerfile
set ml_subscription_id=""
set ml_resource_group=""
set ml_workspace_name=""
set ml_alg_state=""
set ml_alg_author=""
set ml_model_name=""
set ml_image_name=""

powershell -Command "(gc dockerfile.base) -replace '<SUBSCRIPTION_ID>', '%ml_subscription_id%' | Out-File dockerfile -Encoding utf8"
powershell -Command "(gc dockerfile) -replace '<RESOURCE_GROUP>', '%ml_resource_group%' | Out-File dockerfile -Encoding utf8"
powershell -Command "(gc dockerfile) -replace '<WORKSPACE_NAME>', '%ml_workspace_name%' | Out-File dockerfile -Encoding utf8"
powershell -Command "(gc dockerfile) -replace '<STATE>', '%ml_alg_state%' | Out-File dockerfile -Encoding utf8"
powershell -Command "(gc dockerfile) -replace '<AUTHOR>', '%ml_alg_author%' | Out-File dockerfile -Encoding utf8"
powershell -Command "(gc dockerfile) -replace '<MODEL_NAME>', '%ml_model_name%' | Out-File dockerfile -Encoding utf8"
powershell -Command "(gc dockerfile) -replace '<IMAGE_NAME>', '%ml_image_name%' | Out-File dockerfile -Encoding utf8"

docker build -t mlbuild .
:: docker run --name mlbuild --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v c:/Users/%USERNAME%/.azure:/root/.azure mlbuild
docker run --name mlbuild --privileged -v c:/ml_temp/artifacts:/artifacts/ -v c:/Users/%USERNAME%/.azure/:/root/.azure/ mlbuild

:: use env variables & use a git ignore to hide settings.
:: possibly have a local build vs remote build cmd/.sh files.
