import json


def test_get_filtered_exercises_category(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_filtered_exercises
    exercises = get_filtered_exercises(exercise_name=None, category="Strength", muscle_group=None)
    assert len(exercises) == 4
    assert all(exercise.category == "Strength" for exercise in exercises)


def test_get_filtered_exercises_muscle_group(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_filtered_exercises
    exercises = get_filtered_exercises(exercise_name=None, category=None, muscle_group="Glutes")
    assert len(exercises) == 2
    assert all("Glutes" in exercise.muscleGroups for exercise in exercises)


def test_get_filtered_exercises_partial_exercise_name(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_filtered_exercises
    exercises = get_filtered_exercises(exercise_name="Squ", category=None, muscle_group=None)
    assert len(exercises) == 1
    assert exercises[0].exerciseName == "Squat"


def test_get_filtered_exercises_exercise_name(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_filtered_exercises
    exercises = get_filtered_exercises(exercise_name="Squat", category=None, muscle_group=None)
    assert len(exercises) == 1
    assert exercises[0].exerciseName == "Squat"


def test_get_filtered_exercises_none(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_filtered_exercises
    exercises = get_filtered_exercises(exercise_name=None, category=None, muscle_group=None)
    assert len(exercises) == 5


def test_get_exercises_handler_success(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_exercises_handler
    event = {
        "queryStringParameters": {
            "exerciseName": None,
            "category": "Strength",
            "muscleGroup": None
        }
    }
    result = get_exercises_handler(event, None)
    assert result["statusCode"] == 200
    response_body = json.loads(result["body"])
    assert len(response_body) == 4
    assert all(exercise["category"] == "Strength" for exercise in response_body)


def test_get_exercises_handler_success_combined_filters(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_exercises_handler
    event = {
        "queryStringParameters": {
            "exerciseName": "Push",
            "category": "Strength",
            "muscleGroup": "Chest"
        }
    }
    result = get_exercises_handler(event, None)
    assert result["statusCode"] == 200
    response_body = json.loads(result["body"])
    assert len(response_body) == 1
    assert response_body[0]["exerciseName"] == "Push Up"


def test_get_exercises_handler_no_filters(insert_exercises):
    from backend.services.workout_tracker.lambda_get_exercises import get_exercises_handler
    event = {
        "queryStringParameters": {}
    }
    result = get_exercises_handler(event, None)
    assert result["statusCode"] == 200
    response_body = json.loads(result["body"])
    assert len(response_body) == 5


def test_get_exercises_handler_empty_db(workout_exercises_table):
    from backend.services.workout_tracker.lambda_get_exercises import get_exercises_handler
    event = {
        "queryStringParameters": {}
    }
    result = get_exercises_handler(event, None)
    assert result["statusCode"] == 200
    response_body = json.loads(result["body"])
    assert len(response_body) == 0
