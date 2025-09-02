from decimal import Decimal
from http import HTTPStatus
import boto3
from bootcamp_lib.lambda_middleware import (
    BadRequestException, HttpRequestData, InternalServerErrorException, NotFoundException,
    http_request, lambda_logger)
from services.workout_tracker.table_workout_exercises import ExerciseModel, ExerciseTable
from services.workout_tracker.table_workouts import WorkoutTable, WorkoutModel

dynamodb_res = boto3.resource("dynamodb")


def convert_decimal_to_string(data):
    if isinstance(data, Decimal):
        return str(data)
    return data


def get_exercises_by_ids(exercise_ids: list[str]) -> list[ExerciseModel]:
    try:
        exercises = ExerciseTable(dynamodb_res).get_items(keys=[{"exerciseId": id}
                                                                for id in exercise_ids],
                                                          as_dict=True)
        for exercise in exercises:
            exercise["repetitions"] = convert_decimal_to_string(exercise.get("repetitions"))
            exercise["totalSets"] = convert_decimal_to_string(exercise.get("totalSets"))
        return exercises

    except Exception as e:
        raise e


def get_workout_details(workoutId: str) -> WorkoutModel:
    try:
        workout = WorkoutTable(dynamodb_res).get_item(
            key={"workoutId": workoutId},
            as_dict=True,
        )

        if not workout or not workout.get("Item"):
            raise NotFoundException(f"Workout with ID {workoutId} not found.")

        workout_item = workout["Item"]
        workout_item["workoutDuration"] = convert_decimal_to_string(
            workout_item.get("workoutDuration"))

        return workout
    except Exception as e:
        raise e


@http_request()
@lambda_logger(log_input=True)
def get_workout_details_handler(request: HttpRequestData, _):
    workoutId = request.pathParams.get("id")

    if not workoutId:
        raise BadRequestException("Workout ID is required")
    try:
        workout = get_workout_details(workoutId)
        exercise_ids = workout["Item"]["exerciseIds"]
        exercises = get_exercises_by_ids(exercise_ids)
        response = {
            "statusCode": HTTPStatus.OK,
            "workout": workout["Item"],
            "exercises": exercises
        }
        return response
    except NotFoundException as nfe:
        raise NotFoundException(nfe)
    except Exception:
        raise InternalServerErrorException(
            "An error occurred while retrieving the workout details.")
