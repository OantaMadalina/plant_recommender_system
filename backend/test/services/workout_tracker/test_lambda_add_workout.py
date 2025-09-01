import json
import pytest
import boto3
from boto3.dynamodb.conditions import Key
from http import HTTPStatus


def get_workout_by_workout_id(workout_id):
    table = boto3.resource("dynamodb").Table("bootcampengine_test_workouts")
    response = table.query(
        KeyConditionExpression=Key('workoutId').eq(workout_id)
    )
    items = response.get("Items", [])
    return items[0] if items else None


@pytest.fixture(scope='function')
def valid_workout_data():
    return {
        "workoutName": "Morning Workout",
        "workoutDate": "2023-08-17",
        "exerciseIds": ["1", "2"],
        "notes": "Great workout session",
        "workoutDuration": 45,
        "deleted": False
    }


@pytest.fixture(scope='function')
def invalid_workout_name_data():
    return {
        "workoutName": "",
        "workoutDate": "2023-08-17",
        "exerciseIds": ["1", "2"],
        "notes": "Missing workout name",
        "workoutDuration": 45,
        "deleted": False
    }


@pytest.fixture(scope='function')
def invalid_workout_date_data():
    return {
        "workoutName": "Evening Workout",
        "workoutDate": "2023-08-17",
        "exerciseIds": "",  # Invalid date
        "notes": "Missing workout date",
        "workoutDuration": 60,
        "deleted": False
    }


def test_add_workout_success(aws_credentials, valid_workout_data, insert_workouts):
    from services.workout_tracker.lambda_add_workout import add_workout_handler

    event = {
        "body": json.dumps(valid_workout_data)
    }
    result = add_workout_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK
    response_body = json.loads(result["body"])
    workout_id = response_body["body"]["workoutId"]

    assert workout_id is not None, "Expected workout_id to be present, but it was None."

    workout = get_workout_by_workout_id(workout_id)

    assert workout is not None, "Workout not found in DynamoDB."

    assert response_body["body"]["message"] == "The workout was successfully added!"
    assert workout["workoutName"] == valid_workout_data["workoutName"]
    assert workout["workoutDate"] == valid_workout_data["workoutDate"]
    assert workout["exerciseIds"] == valid_workout_data["exerciseIds"]
    assert workout["notes"] == valid_workout_data["notes"]
    assert workout["workoutDuration"] == valid_workout_data["workoutDuration"]
    assert workout["deleted"] == valid_workout_data["deleted"]


def test_add_workout_missing_date_fail(aws_credentials, valid_workout_data):
    from services.workout_tracker.lambda_add_workout import add_workout_handler

    # Remove the required 'workoutDate' field
    invalid_data = valid_workout_data
    del invalid_data["workoutDate"]

    event = {
        "body": json.dumps(invalid_data)
    }
    result = add_workout_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value

    response_body = json.loads(result["body"])
    assert response_body["error"] == "Body field \'workoutDate\' is required"


def test_add_workout_invalid_name_fail(aws_credentials, invalid_workout_name_data):
    from services.workout_tracker.lambda_add_workout import add_workout_handler

    event = {
        "body": json.dumps(invalid_workout_name_data)
    }
    result = add_workout_handler(event, None)

    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value

    response_body = json.loads(result["body"])

    assert response_body["error"] == "Body field \'workoutName\' is required"


def test_add_workout_invalid_date_fail(aws_credentials, invalid_workout_date_data):
    from services.workout_tracker.lambda_add_workout import add_workout_handler

    event = {
        "body": json.dumps(invalid_workout_date_data)
    }
    result = add_workout_handler(event, None)

    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value

    response_body = json.loads(result["body"])

    assert response_body["error"] == "Body field \'exerciseIds\' is required"
