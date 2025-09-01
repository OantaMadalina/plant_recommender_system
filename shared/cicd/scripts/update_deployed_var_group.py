import os
import requests
from requests.auth import HTTPBasicAuth

ORGANIZATION = "vfuk-digital"
PROJECT = "CAVENDISH"
API_VERSION = "api-version=5.0-preview.1"

AZURE_TOKEN = os.environ['PAT']
AZURE_USER = 'azure-user'
ENVIRONMENT = os.environ['STAGE']
COMMIT = os.environ['COMMIT']
BRANCH = os.environ['BRANCH']
GROUP_ID = os.environ['GROUP_ID']
GROUP_NAME = os.environ['GROUP_NAME']

AZURE_URL = f"https://{ORGANIZATION}.visualstudio.com/{PROJECT}/_apis"
VAR_GROUPS_PATH = f"/distributedtask/variablegroups/{GROUP_ID}?{API_VERSION}"


def update_azure_variable_group():
    url = AZURE_URL + VAR_GROUPS_PATH
    r = requests.get(url, auth=HTTPBasicAuth(AZURE_USER, AZURE_TOKEN))
    if r.status_code == 200:
        print("Retrived old variables from Azure DevOps")
        variables = r.json()['variables']

        try:
            variables[ENVIRONMENT + '_commit']['value'] = COMMIT
            variables[ENVIRONMENT + '_branch']['value'] = BRANCH
        except KeyError:
            print("Error in adding new key pair to Azure DevOps")
            exit(0)
        print(f"Setting new deployed version for {ENVIRONMENT}")
        payload_data = {
            "variables": variables,
            "type": "Vsts",
            "id": GROUP_ID,
            "name": GROUP_NAME
        }

        r = requests.put(url, auth=HTTPBasicAuth(
            AZURE_USER, AZURE_TOKEN), json=payload_data)

        if r.status_code == 200:
            print("Added new key pair to Azure DevOps variable group")
            exit(0)
        else:
            print("Error in adding new key pair to Azure DevOps")
            exit(1)
    else:
        print("Error in adding new key pair to Azure DevOps")
        exit(1)


update_azure_variable_group()
