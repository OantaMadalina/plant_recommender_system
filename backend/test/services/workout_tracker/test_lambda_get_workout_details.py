import json
from http import HTTPStatus


def test_get_workout_details_success(aws_credentials, insert_exercises, insert_workouts):
    from services.workout_tracker.lambda_get_workout_details import get_workout_details_handler

    event = {
        'pathParameters': {
            'id': '1'
        }
    }

    result = get_workout_details_handler(event, None)
    body = json.loads(result['body'])

    workout = body.get('workout')
    exercises = body.get('exercises')

    assert result['statusCode'] == HTTPStatus.OK.value
    assert workout['workoutId'] == '1'
    assert workout['workoutName'] == 'Upper Body Workout'
    assert workout['exerciseIds'] == ['1', '3']

    assert len(exercises) == 2
    assert exercises[0]['exerciseId'] == '1'
    assert exercises[0]['exerciseName'] == 'Push Up'
    assert exercises[0]['repetitions'] == '15'
    assert exercises[0]['totalSets'] == '3'
    assert exercises[1]['exerciseId'] == '3'
    assert exercises[1]['exerciseName'] == 'Pull Up'


def test_get_workout_details_non_existent_id(aws_credentials, insert_exercises, insert_workouts):
    from services.workout_tracker.lambda_get_workout_details import get_workout_details_handler

    # Invalid workout ID
    event = {
        'pathParameters': {
            'id': '999'  # Non-existent ID
        }
    }

    result = get_workout_details_handler(event, None)
    body = json.loads(result['body'])

    assert result['statusCode'] == HTTPStatus.NOT_FOUND.value
    assert body['error'] == "Workout with ID 999 not found."


def test_get_workout_details_missing_id(aws_credentials, insert_exercises, insert_workouts):
    from services.workout_tracker.lambda_get_workout_details import get_workout_details_handler

    # No workout ID in the event
    event = {
        'pathParameters': {}
    }

    result = get_workout_details_handler(event, None)
    body = json.loads(result['body'])
    assert result['statusCode'] == HTTPStatus.BAD_REQUEST.value
    assert body['error'] == "Workout ID is required"


def test_get_workout_details_no_exercises(aws_credentials, insert_workouts):
    from services.workout_tracker.lambda_get_workout_details import get_workout_details_handler

    event = {
        'pathParameters': {
            'id': '3'
        }
    }

    result = get_workout_details_handler(event, None)
    body = json.loads(result['body'])

    workout = body['workout']
    exercises = body['exercises']

    assert result['statusCode'] == HTTPStatus.OK

    assert workout['workoutId'] == '3'
    assert workout['exerciseIds'] == []
    assert exercises == []
