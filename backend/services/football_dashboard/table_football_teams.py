from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class FootballTeamModel(DynamoDbModel):
    id: int = 0
    teamName: str = ""
    code: str = ""
    country: str = ""
    founded: int = 0
    isNational: bool = False
    imageUrl: str = ""
    stadiumId: int = 0
    isDeleted: bool = False

    _validations: ClassVar[dict] = {
        "id": {
            "required": True
        },
        "teamName": {
            "required": True
        },
        "code": {
            "required": True
        },
        "country": {
            "required": True
        },
        "founded": {
            "required": True
        },
        "isNational": {
            "required": True
        },
        "imageUrl": {
            "required": False
        },
        "stadiumId": {
            "required": False
        },
        "isDeleted": {
            "required": False
        }
    }


class FootballTeamsTable(DynamodbTable[FootballTeamModel]):
    table = "football-teams-new"
    model_type = FootballTeamModel


class FootballTeamsCache(DynamodbCachedTable[FootballTeamModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = FootballTeamsTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        football_teams = self._table.get_items(keys)
        for football_team in football_teams:
            self._items[football_team.id] = football_team

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.id] = item
