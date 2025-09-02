from typing import ClassVar, List
from dataclasses import dataclass, field

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class FootballGameModel(DynamoDbModel):
    id: int = 0
    firstTeamId: int = 0
    secondTeamId: int = 0
    firstTeamScore: int = 0
    secondTeamScore: int = 0
    gameDateAndTime: str = ""
    scorers: List[str] = field(default_factory=list)

    _validations: ClassVar[dict] = {
        "id": {
            "required": True
        },
        "firstTeamId": {
            "required": True
        },
        "secondTeamId": {
            "required": True
        },
        "firstTeamScore": {
            "required": False
        },
        "secondTeamScore": {
            "required": False
        },
        "gameDateAndTime": {
            "required": False
        },
        "scorers": {
            "required": False
        }
    }


class FootballGamesTable(DynamodbTable[FootballGameModel]):
    table = "football-games"
    model_type = FootballGameModel


class FootballGamesCache(DynamodbCachedTable[FootballGameModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = FootballGamesTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        football_games = self._table.get_items(keys)
        for football_game in football_games:
            self._items[football_game.id] = football_game

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.id] = item
