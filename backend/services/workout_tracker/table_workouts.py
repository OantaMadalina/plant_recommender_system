from typing import ClassVar
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class WorkoutModel(DynamoDbModel):
    workoutId: str = ""
    workoutName: str = ""
    workoutDate: str = ""
    exerciseIds: list[str] = None
    notes: str = ""
    workoutDuration: int = 0
    deleted: bool = False

    _validations: ClassVar[dict] = {
        "workoutId": {
            "required": True
        },
        "workoutName": {
            "required": False
        },
        "workoutDate": {
            "required": True
        },
        "exerciseIds": {
            "required": True
        },
        "notes": {
            "required": False
        },
        "workoutDuration": {
            "required": False
        },
        "deleted": {
            "required": False
        }
    }


class WorkoutTable(DynamodbTable[WorkoutModel]):
    table = "workouts"
    model_type = WorkoutModel


class WorkoutCache(DynamodbCachedTable[WorkoutModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = WorkoutTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: list[dict]):
        workouts = self._table.get_items(keys)
        for workout in workouts:
            self._items[workout.workoutId] = workout

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.workoutId] = item
