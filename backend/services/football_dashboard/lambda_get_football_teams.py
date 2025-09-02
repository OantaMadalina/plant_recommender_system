from dataclasses import dataclass
import os
from typing import List
from boto3.dynamodb.conditions import Attr
import boto3

from bootcamp_lib.lambda_middleware import (
    BadRequestException, HttpRequestData, http_request
)
from bootcamp_lib.logger import Logger
from services.football_dashboard.utils import generate_signed_url
from services.football_dashboard.table_football_teams import FootballTeamModel, FootballTeamsTable

dynamodb_res = boto3.resource("dynamodb", verify=False)


@dataclass
class FootballTeamResponse:
    team: FootballTeamModel
    signedPhotoUrl: str


@dataclass
class FootballTeamsResponse:
    count: int
    allItems: bool
    items: list[FootballTeamResponse]
    sizeLimit: int


def format_query_name(name):
    if not name.isalpha():
        raise BadRequestException("Name must contain only alphabetic characters.")

    return ' '.join(word.capitalize() for word in name.lower().split(' '))


def generate_football_teams_response(items: List[FootballTeamModel], results):
    for item in items:
        s3_key = (
            "FootballDashboard/TeamsImages/"
            f"{item.teamName.replace(' ', '')}.png"
        )
        signed_url = generate_signed_url(os.environ["BOOTCAMP_BUCKET"], s3_key)
        results.append(
            FootballTeamResponse(team=item, signedPhotoUrl=signed_url)
        )


def get_football_teams(ids="", name="", size=50):
    results = []
    table = FootballTeamsTable(dynamodb_res)

    if ids:
        try:
            clean_ids = list(
                set(int(clean_id) for id in ids.split(",") if (clean_id := id.strip()))
            )
        except ValueError as e:
            Logger().error(f"Invalid ID format: {e}")
            raise BadRequestException("Invalid ID format provided.")

        items = table.get_items([{"id": id} for id in clean_ids])
        generate_football_teams_response(items, results)
    elif name:
        formatted_name = format_query_name(name)
        words = formatted_name.split(" ")
        scan_filter = Attr("teamName").contains(words[0])
        for word in words[1:]:
            scan_filter &= Attr("teamName").contains(word)

        items = table.scan(filter=scan_filter, size=size)
        generate_football_teams_response(items, results)
    else:
        items = table.scan(size=size)
        generate_football_teams_response(items, results)

    all_items = len(results) <= size
    results = results[:size]

    return FootballTeamsResponse(
        count=len(results),
        allItems=all_items,
        items=results,
        sizeLimit=size
    )


@http_request
def get_football_teams_handler(event: HttpRequestData, context):
    ids = event.queryParams.get("id", "")
    name = event.queryParams.get("name", "").strip()
    size = int(event.queryParams.get("size", "200"))

    return get_football_teams(ids, name, size)
