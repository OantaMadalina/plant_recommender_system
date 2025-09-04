from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable

@dataclass
class PlantDataModel(DynamoDbModel):
    plantID: int = 0
    plantRating: int = 0
    plantName: str = ""
    soilType: str = ""
    sunlightHours: int = 0
    waterFrequency: str = ""
    fertilizerType: str = ""
    temperature: float = 0.0
    humidity: float = 0.0
    location: str = ""
    age: int = 0

    _validations: ClassVar[dict] = {
        "plantID": {
            "required": True
        },
        "plantRating": {
            "required": True
        },
        "plantName": {
            "required": True
        },
        "soilType": {
            "required": True
        },
        "sunlightHours": {
            "required": True
        },
        "waterFrequency": {
            "required": True
        },
        "fertilizerType": {
            "required": True
        },
        "temperature": {
            "required": True
        },
        "humidity": {
            "required": True
        },
        "location": {
            "required": True
        },
        "age": {
            "required": True
        }
    }


class PlantDataTable(DynamodbTable[PlantDataModel]):
    table = "plant"
    model_type = PlantDataModel


class PlantDataCache(DynamodbCachedTable[PlantDataModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = PlantDataTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        plants = self._table.get_items(keys)
        for plant in plants:
            self._items[plant.plantID] = plant

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.plantID] = item
