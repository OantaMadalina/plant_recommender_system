from __future__ import annotations

import boto3

from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException, NotFoundException
)
from bootcamp_lib.logger import Logger
from services.football_dashboard.table_football_games import FootballGamesTable

dynamodb_res = boto3.resource("dynamodb")


def delete_football_game(game_id: int):
    table = FootballGamesTable(dynamodb_res)
    game = table.delete_item({"id": game_id}, return_values="ALL_OLD")

    if not game.get("Attributes"):
        raise NotFoundException(f"Football game not found for ID {game_id}")


@http_request()
def delete_football_game_handler(event: HttpRequestData, context):
    try:
        game_id = int(event.pathParams.get("id", "").strip())
    except Exception as e:
        Logger().error("Error found trying to get the game ID: " + str(e))
        raise BadRequestException("Error found trying to get the game ID: " + str(e))

    if not game_id:
        raise BadRequestException(f"Invalid football game ID {game_id}")

    return delete_football_game(game_id)
