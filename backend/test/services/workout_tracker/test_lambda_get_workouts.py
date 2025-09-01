from http import HTTPStatus
import json

BOOTCAMP_BUCKET = "test"


def test_get_workouts(aws_credentials, insert_exercises, insert_workouts):
    from services.workout_tracker.lambda_get_workouts import get_workouts_handler

    event = {}
    result = get_workouts_handler(event, None)
    workouts = json.loads(result['body'])
    assert result['statusCode'] == HTTPStatus.OK.value
    assert len(workouts) == 3
    expected_workouts = [
        {
            'workoutId': '1',
            'workoutName': 'Upper Body Workout',
            'workoutDate': '2024-08-27',
            'exerciseIds': ['1', '3'],
            'notes': '',
            'workoutDuration': 10,
            'deleted': False
        },
        {
            'workoutId': '2',
            'workoutName': 'Lower Body Workout',
            'workoutDate': '',
            'exerciseIds': ['2', '5'],
            'notes': '',
            'workoutDuration': None,
            'deleted': False},
        {
            'workoutId': '3',
            'workoutName': 'Core Workout',
            'workoutDate': '',
            'exerciseIds': [],
            'notes': '',
            'workoutDuration': None,
            'deleted': False
        }
    ]
    assert workouts == expected_workouts
