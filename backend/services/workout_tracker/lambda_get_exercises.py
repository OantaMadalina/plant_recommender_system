from logging import Logger
import boto3
from typing import Optional
from boto3.dynamodb.conditions import Attr
from functools import reduce
from operator import and_
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, lambda_logger
)
from services.workout_tracker.table_workout_exercises import (
    ExerciseTable, ExerciseModel
)

dynamodb_res = boto3.resource("dynamodb")


def build_filter_expression(exercise_name: Optional[str],
                            category: Optional[str],
                            muscle_group: Optional[str]):
    filters = []
    if exercise_name:
        filters.append(Attr("exerciseName").contains(exercise_name))

    if category:
        filters.append(Attr("category").contains(category))

    if muscle_group:
        filters.append(Attr("muscleGroups").contains(muscle_group))

    if filters:
        return reduce(and_, filters)

    return None


def get_filtered_exercises(
        exercise_name: Optional[str],
        category: Optional[str],
        muscle_group: Optional[str]) -> list[ExerciseModel]:
    try:
        table = ExerciseTable(dynamodb_res)
        filter_expression = build_filter_expression(exercise_name, category, muscle_group)

        if filter_expression:
            response = table.scan(filter=filter_expression)
        else:
            response = table.scan()

        return response
    except Exception as e:
        Logger().warning(f"Error fetching exercises: {e}")
        raise


@http_request()
@lambda_logger(log_input=True)
def get_exercises_handler(request: HttpRequestData, _):
    exercise_name = request.queryParams.get("exerciseName")
    category = request.queryParams.get("category")
    muscle_group = request.queryParams.get("muscleGroup")

    return get_filtered_exercises(exercise_name, category, muscle_group)
