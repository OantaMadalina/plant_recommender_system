from typing import ClassVar
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class ExerciseModel(DynamoDbModel):
    exerciseId: str = ""
    exerciseName: str = ""
    description: str = ""
    category: str = ""
    youtubeLink: str = ""
    muscleGroups: list[str] = None
    repetitions: int = 0
    totalSets: int = 0

    _validations: ClassVar[dict] = {
        "exerciseId": {
            "required": True
        },
        "exerciseName": {
            "required": True
        },
        "description": {
            "required": False
        },
        "category": {
            "required": False
        },
        "youtubeLink": {
            "required": False
        },
        "muscleGroups": {
            "required": False
        },
        "repetitions": {
            "required": False
        },
        "totalSets": {
            "required": False
        }
    }


class ExerciseTable(DynamodbTable[ExerciseModel]):
    table = "workout-exercices"
    model_type = ExerciseModel


class ExerciseCache(DynamodbCachedTable[ExerciseModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = ExerciseTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: list[dict]):
        exercises = self._table.get_items(keys)
        for exercise in exercises:
            self._items[exercise.exerciseId] = exercises

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.exerciseId] = item
