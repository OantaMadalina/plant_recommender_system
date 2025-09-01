from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable

@dataclass
class PlantDataModel(DynamoDbModel):
    idPlant: str = ""
    namePlant: str = ""
    pricePlant: str = ""
    quantityPlant: str = ""
    descriptionPlant: str = ""
    originCountry: str = ""

    _validations: ClassVar[dict] = {
        "idPlant": {
            "required": True
        },
        "namePlant": {
            "required": True
        },
        "pricePlant": {
            "required": True
        },
        "locationPlant": {
            "required": False
        },
        "quantityPlant": {
            "required": False
        },
        "descriptionPlant": {
            "required": False
        },
        "originCountry": {
            "required": False
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
        plant = self._table.get_items(keys)
        for plant in plant:
            self._items[plant.idPlant] = plant

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.idPlant] = item