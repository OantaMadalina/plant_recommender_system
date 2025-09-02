from datetime import datetime
import json
import boto3
from typing import Dict, List
from bootcamp_lib.logger import Logger
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData,
    BadRequestException, NotFoundException, InternalServerErrorException
)
from services.football_dashboard.table_football_games import FootballGameModel, FootballGamesTable


dynamodb_res = boto3.resource("dynamodb")


def update_football_game(
    game_id: int,
    firstTeamId: int,
    secondTeamId: int,
    firstTeamScore: int,
    secondTeamScore: int,
    gameDateAndTime: str,
    scorers: List[Dict[str, any]]
) -> FootballGameModel:
    if not isinstance(firstTeamId, int) or not isinstance(secondTeamId, int):
        raise BadRequestException("firstTeamId and secondTeamId must be integers.")

    if not isinstance(firstTeamScore, int) or not isinstance(secondTeamScore, int):
        raise BadRequestException("firstTeamScore and secondTeamScore must be integers.")

    table = FootballGamesTable(dynamodb_res)

    existing_game = table.get_item({"id": game_id})

    if not existing_game:
        raise NotFoundException(f"Football game with ID {game_id} not found")

    updated_game = FootballGameModel(**existing_game.to_dict())

    if gameDateAndTime is not None:
        try:
            datetime.strptime(gameDateAndTime, "%Y-%m-%dT%H:%M")
            updated_game.gameDateAndTime = gameDateAndTime
        except ValueError:
            raise BadRequestException(
                "Invalid date and time format. Use ISO 8601 format: YYYY-MM-DDTHH:MM"
            )

    if firstTeamScore < 0 or secondTeamScore < 0:
        raise BadRequestException("Scores cannot be negative")

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

    updated_game.firstTeamScore = firstTeamScore
    updated_game.secondTeamScore = secondTeamScore
    updated_game.scorers = [json.dumps(scorer) for scorer in scorers]

    try:
        table.update_item(
            key={"id": game_id},
            expression=(
                "SET firstTeamId=:firstTeamId, "
                "secondTeamId=:secondTeamId, "
                "firstTeamScore=:firstTeamScore, "
                "secondTeamScore=:secondTeamScore, "
                "gameDateAndTime=:gameDateAndTime, "
                "scorers=:scorers"
            ),
            values={
                ":firstTeamId": updated_game.firstTeamId,
                ":secondTeamId": updated_game.secondTeamId,
                ":firstTeamScore": updated_game.firstTeamScore,
                ":secondTeamScore": updated_game.secondTeamScore,
                ":gameDateAndTime": updated_game.gameDateAndTime,
                ":scorers": updated_game.scorers
            }
        )
    except Exception:
        Logger().exception(f"Error updating football game with ID {game_id}")
        raise InternalServerErrorException(
            f"Unable to update football game with ID {game_id}")

    return updated_game


@http_request(
    request_type="PUT"
)
def update_football_game_handler(event: HttpRequestData, context):
    game_id = event.pathParams.get("id", "").strip()
    if not game_id:
        raise BadRequestException("Football game ID must be provided")

    return update_football_game(
        int(game_id),
        firstTeamId=event.dictBody.get("firstTeamId"),
        secondTeamId=event.dictBody.get("secondTeamId"),
        firstTeamScore=event.dictBody.get("firstTeamScore"),
        secondTeamScore=event.dictBody.get("secondTeamScore"),
        gameDateAndTime=event.dictBody.get("gameDateAndTime"),
        scorers=event.dictBody.get("scorers")
    )
