import boto3
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, lambda_logger
)
from services.workout_tracker.table_workouts import (
    WorkoutTable, WorkoutModel
)

dynamodb_res = boto3.resource("dynamodb")


def get_workouts() -> list[WorkoutModel]:
    try:
        return WorkoutTable(dynamodb_res).scan(size=100)
    except Exception as e:
        raise e


@http_request()
@lambda_logger(log_input=True)
def get_workouts_handler(request: HttpRequestData, _):
    return get_workouts()
