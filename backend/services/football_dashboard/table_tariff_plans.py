from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class TariffPlanModel(DynamoDbModel):
    partNumber: str = ""
    packageName: str = ""
    contractLength: int = 0
    contractLengthUOM: str = ""
    lineRentalAmount: float = 0.0
    vatCode: float = 0.0
    priceRiseAmount_1: float = 0.0
    priceRiseAmount_2: float = 0.0
    priceRiseAmount_3: float = 0.0
    OOCPriceRise: float = 0.0
    deleted: bool = False

    _validations: ClassVar[dict] = {
        "partNumber": {
            "required": True
        },
        "packageName": {
            "required": False
        },
        "contractLength": {
            "required": True
        },
        "contractLengthUOM": {
            "required": True
        },
        "lineRentalAmount": {
            "required": True
        },
        "vatCode": {
            "required": True
        },
        "priceRiseAmount_1": {
            "required": False
        },
        "priceRiseAmount_2": {
            "required": False
        },
        "priceRiseAmount_3": {
            "required": False
        },
        "OOCPriceRise": {
            "required": False
        },
        "deleted": {
            "required": False
        }
    }


class TariffPlansTable(DynamodbTable[TariffPlanModel]):
    table = "tariff-plans"
    model_type = TariffPlanModel


class TariffPlansCache(DynamodbCachedTable[TariffPlanModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = TariffPlansTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        tariff_plans = self._table.get_items(keys)
        for tariff_plan in tariff_plans:
            self._items[tariff_plan.partNumber] = tariff_plan

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.partNumber] = item
