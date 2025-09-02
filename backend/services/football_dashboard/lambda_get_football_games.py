from dataclasses import dataclass
import json
from xml.dom.minidom import Attr
import boto3

from bootcamp_lib.lambda_middleware import BadRequestException, HttpRequestData, http_request
from services.football_dashboard.table_football_games import (
    FootballGameModel, FootballGamesTable
)

dynamodb_res = boto3.resource("dynamodb", verify=False)


@dataclass
class FootballGamesResponse:
    count: int
    allItems: bool
    items: list[FootballGameModel]
    sizeLimit: int


def get_football_games(ids: str = "", team_id: str = "", size: int = 200):
    results = []
    football_games_table = FootballGamesTable(dynamodb_res)

    if ids:
        clean_ids = list(set(int(clean_id) for id in ids.split(",") if (clean_id := id.strip())))
        games = football_games_table.get_items([{"id": id} for id in clean_ids])

        for game in games:
            game.scorers = [json.loads(scorer) for scorer in game.scorers]
            results.append(game)
    elif team_id:
        # Get teams by game id, if team takes part of a game.
        scan_filter = Attr("firstTeamId").eq(team_id) | Attr("secondTeamId").eq(team_id)
        games = football_games_table.scan(filter=scan_filter, size=size)

        for game in games:
            game.scorers = [json.loads(scorer) for scorer in game.scorers]
            results.append(game)
    else:
        games = football_games_table.scan(size=size)

        for game in games:
            game.scorers = [json.loads(scorer) for scorer in game.scorers]
            results.append(game)

    all_items = len(results) <= size
    results = results[:size]

    return FootballGamesResponse(
        count=len(results),
        allItems=all_items,
        items=results,
        sizeLimit=size
    )


@http_request
def get_football_games_handler(event: HttpRequestData, context):
    ids = event.queryParams.get("id", "")
    try:
        size = int(event.queryParams.get("size", "200"))
    except ValueError:
        raise BadRequestException("Invalid 'size' parameter, must be an integer.")
    team_id = event.queryParams.get("team_id", "")

    if team_id:
        team_id = int(team_id)

    return get_football_games(ids, team_id, size)
