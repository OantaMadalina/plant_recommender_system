import json
import os
import argparse

import requests
from requests.auth import HTTPBasicAuth


ORGANIZATION = "vfuk-digital"
PROJECT = "CAVENDISH"
API_VERSION = "api-version=5.0-preview.1"

AZURE_URL = f"https://{ORGANIZATION}.visualstudio.com/{PROJECT}/_apis"

AZURE_TOKEN = os.environ["PAT"]
AZURE_USER = "azure-user"


def fetch_azure_group(group_id: str) -> dict:
    VAR_GROUPS_PATH = f"/distributedtask/variablegroups/{group_id}?{API_VERSION}"
    r = requests.get(AZURE_URL + VAR_GROUPS_PATH, auth=HTTPBasicAuth(AZURE_USER, AZURE_TOKEN))
    if r.status_code != 200 or r.text == "null":
        raise Exception("Error fetching variables")
    return r.json()


def get_azure_variables(group_id: str):
    try:
        vars = fetch_azure_group(group_id)["variables"]
        print(json.dumps({name: val["value"] for name, val in vars.items()}, indent=2))
    except Exception as e:
        print(e)
        exit(1)


def update_azure_variables(group_id: str, variables: dict):
    try:
        group = fetch_azure_group(group_id)
    except Exception as e:
        print(e)
        exit(1)

    cur_vars = {k: v["value"] for k, v in group["variables"].items()}
    cur_vars.update(variables)
    payload_vars = {k: {"value": v} for k, v in cur_vars.items()}

    VAR_GROUPS_PATH = f"/distributedtask/variablegroups/{group_id}?{API_VERSION}"
    payload_data = {
        "variables": payload_vars,
        "type": group["type"],
        "id": group["id"],
        "name": group["name"]
    }
    r = requests.put(
        AZURE_URL + VAR_GROUPS_PATH, auth=HTTPBasicAuth(AZURE_USER, AZURE_TOKEN), json=payload_data)
    if r.status_code != 200:
        print("Error updating variables")

    print("Variables successfully updated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch/update Azure Devops variables")
    parser.add_argument("--group-id", default=None, help="Group ID", required=True)
    parser.add_argument("--fetch", action="store_true", default=False, help="Fetch variables")
    parser.add_argument("--update", action="store_true", default=False, help="Update variables")
    parser.add_argument("--value", action="append", nargs='+', help="Variable pair")
    args = parser.parse_args()

    if args.update:
        values = {}
        for value in args.value:
            values[value[0]] = value[1]
        update_azure_variables(args.group_id, values)

    if args.fetch:
        get_azure_variables(args.group_id)
