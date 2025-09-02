from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class RegionsModel(DynamoDbModel):
    regionName: str = ""
    regionSummary: str = ""
    regionDescription: str = ""
    regionImage: str = ""
    deleted: bool = False

    _validations: ClassVar[dict] = {
        "regionName": {
            "required": True
        },
        "regionSummary": {
            "required": False
        },
        "regionDescription": {
            "required": False
        },
        "regionImage": {
            "required": False
        },
        "deleted": {
            "required": False
        }
    }


class RegionsTable(DynamodbTable[RegionsModel]):
    table = "regions"
    model_type = RegionsModel


class RegionsCache(DynamodbCachedTable[RegionsModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = RegionsTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        regions = self._table.get_items(keys)
        for region in regions:
            self.items[region.regionName] = region

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.regionName] = item
