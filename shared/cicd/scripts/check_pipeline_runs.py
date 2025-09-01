from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.pipelines.pipelines_client import PipelinesClient
import time
import os
import sys

# Access token for ADO, set as environment variable in the pipeline yaml
token = os.environ["PAT"]

# ADO predefined variables
my_definition_id = int(os.environ["SYSTEM_DEFINITIONID"])
my_build_id = int(os.environ["BUILD_BUILDID"])
my_project = os.environ["SYSTEM_TEAMPROJECT"]
my_organization_url = os.environ["SYSTEM_TASKDEFINITIONSURI"]

# Setting up connection to ADO
credentials = BasicAuthentication('', token)
connection = Connection(base_url=my_organization_url, creds=credentials)
pipeline_c: PipelinesClient = connection.clients_v7_0.get_pipelines_client()

# Checking the pipeline definition id for any existing runs
# If any active runs with run id lower than current run id, wait until all are completed before continuing current run
while not len([run for run in pipeline_c.list_runs(project=my_project, pipeline_id=my_definition_id) if
              run.state == "inProgress" and run.id <= my_build_id]) == 1:

    print("Active runs detected for this pipeline:")

    # Flush required for ADO agent to print statement live, otherwise all the prints happen at the end
    sys.stdout.flush()

    # Print current run id and ids for any active/queued runs
    print([run.id for run in pipeline_c.list_runs(project=my_project, pipeline_id=my_definition_id) if
          run.state == "inProgress" and run.id <= my_build_id])

    # Flush required for ADO agent to print statement live, otherwise all the prints happen at the end
    sys.stdout.flush()

    # Sleep for 20 seconds before attempting to initiate the run again
    time.sleep(20)

print("No active runs detected for this pipeline, proceeding with current run.")
