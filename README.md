# COMP3211 - Distributed Systems

Coursework 2 - Serverless speed camera workflow

## Runnng solution

Requirements:
- Python 3.10
- NPM

### Install azure function core tools

```
npm install --global azure-functions-core-tools
```


### Run locally

```
func start
```

### Deploy to Azure function app

```
func azure functionapp publish vehicle-analysis --build-remote
```

