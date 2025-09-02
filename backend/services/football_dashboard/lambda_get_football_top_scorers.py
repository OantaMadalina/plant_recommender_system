from dataclasses import dataclass
from typing import List
import boto3
from collections import defaultdict
import json  # To parse the scorers JSON strings

from bootcamp_lib.lambda_middleware import (
    HttpRequestData, InternalServerErrorException, http_request
)
from bootcamp_lib.logger import Logger
from services.football_dashboard.table_football_games import FootballGamesTable

dynamodb_res = boto3.resource("dynamodb", verify=False)


@dataclass
class TopGoalScorer:
    player_id: int
    goals_scored: int


@dataclass
class TopGoalScorersResponse:
    count: int
    items: List[TopGoalScorer]


def compute_top_goal_scorers() -> List[TopGoalScorer]:
    football_games_table = FootballGamesTable(dynamodb_res)

    try:
        games = football_games_table.scan(as_dict=True)
    except Exception as e:
        Logger().exception("Failed to retrieve football games from DynamoDB: " + e)
        raise InternalServerErrorException("Error retrieving football games from the database.")

    goal_scorers = defaultdict(int)

    for game in games:
        scorers_data = game.get('scorers', [])
        for scorer_json in scorers_data:
            scorer = json.loads(scorer_json)
            player_id = int(scorer['playerId'])
            goals_scored = len(scorer['minutes'])
            goal_scorers[player_id] += goals_scored

    goal_scorers_list = [
        {
            "player_id": player_id,
            "goals_scored": goals_scored
        }
        for player_id, goals_scored in goal_scorers.items()
    ]

    # Sort the goal scorers by number of goals, in descending order
    goal_scorers_list.sort(key=lambda x: x['goals_scored'], reverse=True)

    top_20_scorers = goal_scorers_list[:20]

    return [TopGoalScorer(**scorer) for scorer in top_20_scorers]


@http_request
def get_football_top_scorers_handler(event: HttpRequestData, context):
    top_scorers = compute_top_goal_scorers()

    return TopGoalScorersResponse(
        count=len(top_scorers),
        items=top_scorers
    )


if __name__ == "__main__":
    print(get_football_top_scorers_handler({}, None))
