# Serverless speed camera workflow

## Runnng solution

Requirements:
- Python 3.10
- PIP
- NPM

### Install azure function core tools

```
npm install --global azure-functions-core-tools
```

### Create database

Azure SQL database using free vCore offer.

### Create blob storage

Set connection strings and role permissions.

### Run function locally

```
func start
```

### Create Azure Function App
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?
```
az functionapp create --resource-group AzureFunctionsQuickstart-rg --consumption-plan-location westeurope --runtime python --runtime-version <PYTHON_VERSION> --functions-version 4 --name <APP_NAME> --os-type linux --storage-account <STORAGE_NAME>
```

### Deploy to Azure Function App

Make sure Function App is currently running before running command.

```
func azure functionapp publish vehicle-analysis --build-remote
```

