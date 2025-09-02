from typing import ClassVar, List
from dataclasses import dataclass

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class FootballPlayerModel(DynamoDbModel):
    id: int = 0
    fullName: str = ""
    firstName: str = ""
    lastName: str = ""
    age: int = 0
    nationality: str = ""
    height: str = ""
    weight: str = ""
    isInjured: bool = False
    imageUrl: str = ""
    teamId: int = 0
    leagueId: int = 0
    fieldPosition: str = ""
    isCaptain: bool = False
    goalsTotal: int = 0
    assists: int = 0

    _validations: ClassVar[dict] = {
        "id": {
            "required": True
        },
        "fullName": {
            "required": True
        },
        "firstName": {
            "required": True
        },
        "lastName": {
            "required": True
        },
        "age": {
            "required": True
        },
        "nationality": {
            "required": True
        },
        "height": {
            "required": False
        },
        "weight": {
            "required": False
        },
        "isInjured": {
            "required": False
        },
        "imageUrl": {
            "required": True
        },
        "teamId": {
            "required": True
        },
        "leagueId": {
            "required": True
        },
        "fieldPosition": {
            "required": True
        },
        "isCaptain": {
            "required": False
        },
        "goalsTotal": {
            "required": False
        },
        "assists": {
            "required": False
        }
    }


class FootballPlayersTable(DynamodbTable[FootballPlayerModel]):
    table = "football-players-new"
    model_type = FootballPlayerModel


class FootballPlayerCache(DynamodbCachedTable[FootballPlayerModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = FootballPlayersTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        football_players = self._table.get_items(keys)
        for football_player in football_players:
            self._items[football_player.id] = football_player

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.id] = item
