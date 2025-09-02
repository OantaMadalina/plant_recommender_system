from __future__ import annotations
import json
from datetime import datetime, timezone

import boto3
from typing import Dict, List

from bootcamp_lib.logger import Logger
from bootcamp_lib.lambda_middleware import (
    ConflictException, http_request, HttpRequestData, InternalServerErrorException,
    BadRequestException
)
from services.football_dashboard.table_football_games import FootballGameModel, FootballGamesTable
from services.football_dashboard.table_football_teams import FootballTeamsTable

dynamodb_res = boto3.resource("dynamodb", verify=False)


def create_custom_id(firstTeamId: int, secondTeamId: int, gameDateAndTime: str) -> int:
    year = datetime.fromisoformat(gameDateAndTime).year
    custom_id_str = f"{firstTeamId}{secondTeamId}{year}"
    custom_id = int(custom_id_str)

    return custom_id


def create_football_game(
    firstTeamId: int,
    secondTeamId: int,
    firstTeamScore: int,
    secondTeamScore: int,
    gameDateAndTime: str,
    scorers: List[Dict[str, any]]
) -> FootballGameModel:
    football_games_table = FootballGamesTable(dynamodb_res)
    football_teams_table = FootballTeamsTable(dynamodb_res)

    if not isinstance(firstTeamId, int) or not isinstance(secondTeamId, int):
        raise BadRequestException("firstTeamId and secondTeamId must be integers.")

    if not isinstance(firstTeamScore, int) or not isinstance(secondTeamScore, int):
        raise BadRequestException("firstTeamScore and secondTeamScore must be integers.")

    if firstTeamScore < 0 or secondTeamScore < 0:
        raise BadRequestException("Scores cannot be negative")

    first_team = football_teams_table.get_item({"id": firstTeamId})
    second_team = football_teams_table.get_item({"id": secondTeamId})

    if not first_team:
        raise BadRequestException(f"Team with id {firstTeamId} does not exist.")
    if not second_team:
        raise BadRequestException(f"Team with id {secondTeamId} does not exist.")

    try:
        datetime.strptime(gameDateAndTime, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise BadRequestException(
            "Invalid date and time format. Use ISO 8601 format: YYYY-MM-DDTHH:MM"
        )

    custom_id = create_custom_id(firstTeamId, secondTeamId, gameDateAndTime)
    game = football_games_table.get_item({"id": custom_id})
    if game:
        raise ConflictException("This game was already created for the current season.")

    first_team_scorers = [scorer for scorer in scorers if scorer["teamId"] == firstTeamId]
    second_team_scorers = [scorer for scorer in scorers if scorer["teamId"] == secondTeamId]

    total_first_team_goals = sum(len(scorer["minutes"]) for scorer in first_team_scorers)
    total_second_team_goals = sum(len(scorer["minutes"]) for scorer in second_team_scorers)

    if total_first_team_goals != firstTeamScore:
        raise BadRequestException(
            "Number of scorers for the first team must match the first team score"
        )

    if total_second_team_goals != secondTeamScore:
        raise BadRequestException(
            "Number of scorers for the second team must match the second team score"
        )

    for scorer in scorers:
        if not all(k in scorer for k in ("playerId", "teamId", "minutes")):
            raise BadRequestException(
                f"Scorer {scorer.get('playerId')} must have playerId, teamId, and minutes"
            )

    game = FootballGameModel(
        id=custom_id,
        firstTeamId=firstTeamId,
        secondTeamId=secondTeamId,
        firstTeamScore=firstTeamScore,
        secondTeamScore=secondTeamScore,
        gameDateAndTime=gameDateAndTime,
        scorers=[json.dumps(scorer) for scorer in scorers]
    )

    try:
        football_games_table.put_item(game)
    except Exception as e:
        Logger().exception("Error creating football game. Error: " + e)
        raise InternalServerErrorException("Unable to create football game")

    return game


@http_request(
    request_type="POST",
    validation={
        "firstTeamId": {"required": True},
        "secondTeamId": {"required": True},
    }
)
def create_football_game_handler(event: HttpRequestData, context):
    firstTeamId = event.dictBody.get("firstTeamId")
    secondTeamId = event.dictBody.get("secondTeamId")
    firstTeamScore = event.dictBody.get("firstTeamScore", 0)
    secondTeamScore = event.dictBody.get("secondTeamScore", 0)
    gameDateAndTime = event.dictBody.get(
        "gameDateAndTime",
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    scorers = event.dictBody.get("scorers", {})

    return create_football_game(
        firstTeamId,
        secondTeamId,
        firstTeamScore,
        secondTeamScore,
        gameDateAndTime,
        scorers
    )
