from dataclasses import dataclass
from typing import List
import boto3
from collections import defaultdict

from bootcamp_lib.lambda_middleware import (
    HttpRequestData, InternalServerErrorException, http_request
)
from bootcamp_lib.logger import Logger
from services.football_dashboard.table_football_games import FootballGamesTable


dynamodb_res = boto3.resource("dynamodb", verify=False)


@dataclass
class FootballStanding:
    team_id: int
    position: int
    points: int
    goals_scored: int
    goals_conceded: int
    games_played: int


@dataclass
class FootballStandingsResponse:
    count: int
    items: List[FootballStanding]


def compute_standings() -> List[FootballStanding]:
    football_games_table = FootballGamesTable(dynamodb_res)

    try:
        games = football_games_table.scan(as_dict=True)
    except Exception as e:
        Logger().exception("Failed to scan football games from DynamoDB: " + e)
        raise InternalServerErrorException("Unable to retrieve football games from the database.")

    standings = defaultdict(
        lambda: {"team_id": 0, "points": 0, "goals_scored": 0, "goals_conceded": 0, "games_played": 0}
    )

    for game in games:
        first_team_id = int(game['firstTeamId'])
        second_team_id = int(game['secondTeamId'])
        # convert to int because of the way it is stored in db, it might be Decimal
        first_team_score = int(game['firstTeamScore'])
        second_team_score = int(game['secondTeamScore'])

        standings[first_team_id]['team_id'] = first_team_id
        standings[first_team_id]['games_played'] += 1
        standings[first_team_id]['goals_scored'] += first_team_score
        standings[first_team_id]['goals_conceded'] += second_team_score
        if first_team_score > second_team_score:
            standings[first_team_id]['points'] += 3
        elif first_team_score == second_team_score:
            standings[first_team_id]['points'] += 1

        standings[second_team_id]['team_id'] = second_team_id
        standings[second_team_id]['games_played'] += 1
        standings[second_team_id]['goals_scored'] += second_team_score
        standings[second_team_id]['goals_conceded'] += first_team_score
        if second_team_score > first_team_score:
            standings[second_team_id]['points'] += 3
        elif second_team_score == first_team_score:
            standings[second_team_id]['points'] += 1

    standings_list = list(standings.values())

    standings_list.sort(
        key=lambda x: (x['points'], x['goals_scored'] - x['goals_conceded']),
        reverse=True
    )

    for idx, team in enumerate(standings_list):
        team['position'] = idx + 1

    print(standings_list)

    return [FootballStanding(**team) for team in standings_list]


@http_request
def get_football_standings_handler(event: HttpRequestData, context):
    standings = compute_standings()

    return FootballStandingsResponse(
        count=len(standings),
        items=standings
    )
