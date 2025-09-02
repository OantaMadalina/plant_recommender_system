from dataclasses import dataclass
import os
from typing import List
from boto3.dynamodb.conditions import Attr, Key
import boto3
from bootcamp_lib.logger import Logger

from bootcamp_lib.lambda_middleware import BadRequestException, HttpRequestData, http_request
from services.football_dashboard.utils import generate_signed_url
from services.football_dashboard.table_football_players import (
    FootballPlayersTable,
    FootballPlayerModel
)

dynamodb_res = boto3.resource("dynamodb", verify=False)


@dataclass
class FootballPlayerResponse:
    player: FootballPlayerModel
    signedPhotoUrl: str


@dataclass
class FootballPlayersResponse:
    count: int
    allItems: bool
    items: list[FootballPlayerResponse]
    sizeLimit: int


def format_query_name(name):
    if not name.isalpha():
        raise BadRequestException("Name must contain only alphabetic characters.")

    return ' '.join(word.capitalize() for word in name.lower().split(' '))


def generate_football_players_response(items: List[FootballPlayerModel], results):
    for item in items:
        s3_key = (
            "FootballDashboard/PlayersImages/"
            f"{item.fullName.replace(' ', '')}.png"
        )
        signed_url = generate_signed_url(os.environ["BOOTCAMP_BUCKET"], s3_key)
        results.append(
            FootballPlayerResponse(player=item, signedPhotoUrl=signed_url)
        )


def get_football_players(ids="", name="", team_id=0, size=50):
    results = []
    football_players_table = FootballPlayersTable(dynamodb_res)

    if ids:
        try:
            clean_ids = list(
                set(int(clean_id) for id in ids.split(",") if (clean_id := id.strip()))
            )
        except ValueError:
            raise BadRequestException("IDs must be a comma-separated list of integers.")

        items = football_players_table.get_items([{"id": id} for id in clean_ids])
        generate_football_players_response(items, results)
    elif name:
        formatted_name = format_query_name(name)
        words = formatted_name.split(" ")
        scan_filter = Attr("fullName").contains(words[0])
        for word in words[1:]:
            scan_filter &= Attr("fullName").contains(word)

        items = football_players_table.scan(filter=scan_filter, size=size)
        generate_football_players_response(items, results)
    elif team_id:
        key_condition = Key("teamId").eq(team_id)
        items = football_players_table.query(
            key_condition=key_condition,
            index_name="teamIdIndex",
            size=size,
        ).items
        generate_football_players_response(items, results)
    else:
        Logger().error(f"ID or name must be specified {team_id}")
        raise BadRequestException("ID or name must be specified")

    all_items = len(results) <= size
    results = results[:size]

    return FootballPlayersResponse(
        count=len(results),
        allItems=all_items,
        items=results,
        sizeLimit=size
    )


@http_request
def get_football_players_handler(event: HttpRequestData, context):
    ids = event.queryParams.get("id", "")
    name = event.queryParams.get("name", "").strip()
    try:
        team_id = int(event.queryParams.get("teamId", 0))
        size = int(event.queryParams.get("size", "200"))
    except ValueError:
        raise BadRequestException("Invalid 'teamId' or 'size' parameter, must be an integer.")

    return get_football_players(ids, name, team_id, size)
