from typing import List
from uuid import uuid4
from dataclasses import dataclass, field
from datetime import datetime, timezone


from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class SongLocationModel(DynamoDbModel):
    locationId: str = ""
    imagePath: str = ""
    description: str = ""
    latitude: str = ""
    longitude: str = ""
    createdAt: str = ""

    def __post_init__(self):
        super().__post_init__()
        if not self.locationId:
            self.locationId = str(uuid4())

        if not self.createdAt:
            self.createdAt = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


@dataclass
class SongModel(DynamoDbModel):
    songId: str = ""
    songName: str = ""
    artist: str = ""
    album: str = ""
    searchToken: str = ""
    YTURL: str = ""
    locations: List[SongLocationModel] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        if not self.songId:
            self.songId = str(uuid4())


class SongsTable(DynamodbTable[SongModel]):
    table = "songs"
    model_type = SongModel


class SongsCache(DynamodbCachedTable[SongModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = SongsTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        songs = self._table.get_items(keys)
        for song in songs:
            self._items[song.songId] = song

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.songId] = item
