from dataclasses import dataclass, field

from bootcamp_lib.dynamodb_model import DynamoDbModel


@dataclass
class SongResponse(DynamoDbModel):
    songId: str = ""
    message: str = ""


@dataclass
class SongLocationResponse(SongResponse):
    location: dict = field(default_factory=dict)
