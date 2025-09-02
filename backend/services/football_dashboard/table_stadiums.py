from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class StadiumModel(DynamoDbModel):
    id: int = 0
    stadiumName: str = ""
    address: str = ""
    city: str = ""
    stadiumCapacity: int = 0
    surface: str = ""
    imageUrl: str = ""
    teamId: int = 0
    isDeleted: bool = False

    _validations: ClassVar[dict] = {
        "id": {
            "required": True
        },
        "stadiumName": {
            "required": True
        },
        "address": {
            "required": True
        },
        "city": {
            "required": True
        },
        "stadiumCapacity": {
            "required": True
        },
        "surface": {
            "required": True
        },
        "imageUrl": {
            "required": False
        },
        "teamId": {
            "required": True
        },
        "isDeleted": {
            "required": False
        }
    }


class StadiumsTable(DynamodbTable[StadiumModel]):
    table = "football-stadiums-new"
    model_type = StadiumModel


class StadiumsCache(DynamodbCachedTable[StadiumModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = StadiumsTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        stadiums = self._table.get_items(keys)
        for stadium in stadiums:
            self._items[stadium.id] = stadium

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.id] = item
