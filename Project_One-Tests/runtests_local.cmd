:: Remove containers that could be running
docker stop mltests
docker rm mltests

:: Build AML Container
:: cd ..
:: cd ./Project_One
:: docker build -t mlbuild .
:: docker run --name mlbuild --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock mlbuild

REM cd ..
REM cd ./Project_One
REM cmd runbuild_local.cmd

:: TODO: Get generated container ID & replace token in docker file
powershell -Command "$dict = (gc c:/ml_temp/artifacts/artifacts.json) | ConvertFrom-JSON; (gc dockerfile.base) -replace '<AZMLGENERATEDCONTAINER>', $dict.image_location | Out-File dockerfile -Encoding utf8"

cd ..
cd ./Project_One-Tests
docker build -t mltests .

if not exist "C:\ml_temp\artifacts\test_results" mkdir C:\ml_temp\artifacts\test_results
docker run --name mltests --privileged -v c:/ml_temp/artifacts/test_results:/var/azureml-app/tests/junit mltests