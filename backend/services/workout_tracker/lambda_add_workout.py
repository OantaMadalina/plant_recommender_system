from http import HTTPStatus
import uuid
import boto3
from typing import Dict, Any
from dataclasses import asdict
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, InternalServerErrorException, http_request, lambda_logger
)
from services.workout_tracker.table_workouts import (
    WorkoutTable, WorkoutModel
)

dynamodb_res = boto3.resource("dynamodb")


def add_workout(data: Dict[str, Any]) -> Dict[str, Any]:
    data_without_workout_id = {key: value for key, value in data.items() if key != 'workoutId'}

    workout = WorkoutModel(
        workoutId=str(uuid.uuid4()),
        **data_without_workout_id
    )

    WorkoutTable(dynamodb_res).put_item(workout)
    return asdict(workout)


@http_request(
    request_type="POST",
    validation={
        "workoutName": {"required": True},
        "workoutDate": {"required": True},
        "exerciseIds": {"required": True}
    })
@lambda_logger(log_input=True)
def add_workout_handler(request: HttpRequestData, _):
    dictBody = request.dictBody
    workoutId = ""

    try:
        new_workout = add_workout(dictBody)
        workoutId = new_workout["workoutId"]

        http_status = HTTPStatus.OK
        message = "The workout was successfully added!"
        response = {
            "statusCode": http_status,
            "body": {
                "message": message,
                "workoutId": workoutId
            }
        }
        return response
    except Exception:
        raise InternalServerErrorException("An unexpected error occurred while adding the workout.")
