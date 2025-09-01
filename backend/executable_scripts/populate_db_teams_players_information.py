import http.client
import json
import os
import time
from typing import Any

import boto3
import requests
import tempfile
from bootcamp_lib.logger import Logger
from bootcamp_lib.s3 import CavendishS3
from services.football_dashboard.table_football_teams import FootballTeamModel, FootballTeamsTable
from services.football_dashboard.table_football_players import (
    FootballPlayerModel, FootballPlayersTable
)
from services.football_dashboard.table_stadiums import StadiumModel, StadiumsTable

dynamodb_res = boto3.resource("dynamodb", verify=False)
bootcamp_s3 = CavendishS3(os.environ["BOOTCAMP_BUCKET"])


# Calls the endpoint given as an argument with optional params to this host:
# "v3.football.api-sports.io"
def call_api(endpoint, params=None):
    if params is None:
        params = {}
    parameters = '?' + \
        '&'.join([f'{key}={value}' for key,
                 value in params.items()]) if params else ''

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': os.environ["FOOTBALL_API_KEY"]
    }

    try:
        conn.request("GET", f"/{endpoint}{parameters}", headers=headers)
        res = conn.getresponse()

        data = res.read().decode("utf-8")

        try:
            response = json.loads(data)
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decoding error: {str(e)}")

    except http.client.HTTPException as e:
        raise Exception(f"HTTP exception occurred: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    finally:
        # Close the connection regardless of the try-except result
        conn.close()

    return response


def get_players_data(league, season, page=1, players=None):
    if players is None:
        players = []

    while True:
        response = call_api(
            'players', {'league': league, 'season': season, 'page': page})

        # We have a rate limit of 10 requests per minute for a certain endpoint,
        # therefore, we wait for a minute if we reach this limit, which is marked
        # by the Rate Limit error in the response.
        if response['errors'] and response['errors']['rateLimit']:
            time.sleep(60)
            continue

        players.extend(response['response'])
        break

    if (response['paging']['current'] < response['paging']['total']
            and response['paging']['current'] < 3):
        page = response['paging']['current'] + 1
        players = get_players_data(league, season, page, players)

    return players


def send_get_request_with_retry(URL, retry=1):
    r = None

    for _ in range(retry):
        try:
            r = requests.get(URL, stream=True)
            if r.status_code not in [200, 404]:
                time.sleep(1)
            else:
                break
        except requests.exceptions.ConnectionError:
            print(f"Failed to get photo from {URL}.")

    return r


def download_and_upload_image(
    football_resource: FootballPlayerModel | StadiumModel | FootballTeamModel | Any
):
    # Determine the S3 path based on the type of football_resource
    if isinstance(football_resource, FootballPlayerModel):
        s3_path = (
            "FootballDashboard/PlayersImages/"
            f"{football_resource.fullName.replace(' ', '')}.png"
        )
    elif isinstance(football_resource, StadiumModel):
        s3_path = (
            "FootballDashboard/StadiumsImages/"
            f"{football_resource.stadiumName.replace(' ', '')}.png"
        )
    elif isinstance(football_resource, FootballTeamModel):
        s3_path = f"FootballDashboard/TeamsImages/{football_resource.teamName.replace(' ', '')}.png"
    else:
        raise ValueError("Unsupported football_resource type")

    response = send_get_request_with_retry(football_resource.imageUrl, 4)
    if response.status_code == 200:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            for chunk in response.iter_content(1024):
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
            print(tmp_file_path)

        # Upload the file to S3
        bootcamp_s3.upload_file(
            tmp_file_path,
            s3_path
        )

        # Clean up the temporary file
        os.remove(tmp_file_path)
    else:
        print(f"Failed to download OR upload {football_resource.name}'s photo")


if __name__ == "__main__":
    file_path = "C:/Users/RosuA3/Downloads/teams_and_players_output.json"
    football_teams_table = FootballTeamsTable(dynamodb_res)
    stadiums_table = StadiumsTable(dynamodb_res)
    football_players_table = FootballPlayersTable(dynamodb_res)

    # GET teams & stadiums data
    response = call_api('teams', {'league': 39, 'season': 2021})
    teams = response['response']

    # Old code for writing output JSON file
    # data = {
    #     "teams": teams,
    #     "players": players
    # }
    # with open(file_path, 'w') as f:
    #     json.dump(data, f, indent=2)
    # ftbl = football_teams_table.scan(projection="id")
    # print(ftbl)

    # print(football_teams_table.get_item(
    #     {"id": "1"}))

    football_teams = []
    stadiums = []

    # Create resource lists & upload resources' images to S3
    for team in teams:
        team_data = team['team']
        venue_data = team['venue']

        team_data['stadiumId'] = venue_data['id']
        # The API returns a dict with link to the team image found at
        # the 'logo' key, but we use an 'image' field for uniformity
        team_data['imageUrl'] = team_data.pop('logo')
        team_data['teamName'] = team_data.pop('name')
        team_data['isNational'] = team_data.pop('national')

        football_team = FootballTeamModel(**team_data)
        football_teams.append(football_team)
        download_and_upload_image(football_team)

        venue_data['teamId'] = team_data['id']

        venue_data['stadiumName'] = venue_data.pop('name')
        venue_data['imageUrl'] = venue_data.pop('image')

        stadium = StadiumModel(**venue_data)
        stadiums.append(stadium)
        download_and_upload_image(stadium)

    # Add football team instances to db table
    try:
        football_teams_table.put_items(football_teams)
    except Exception:
        Logger().exception("Error adding football teams list in db table")

    # Add stadium instances to db table
    try:
        stadiums_table.put_items(stadiums)
    except Exception:
        Logger().exception("Error adding stadiums list in db table")

    # GET players data
    players = get_players_data(39, 2021)

    football_players = []

    # Create players list & upload players' images to S3
    for player in players:
        player_info = player['player']
        stats = player['statistics'][0]

        football_player = FootballPlayerModel(
            id=player_info['id'],
            fullName=player_info['name'],
            firstName=player_info['firstname'],
            lastName=player_info['lastname'],
            age=player_info['age'],
            nationality=player_info['nationality'],
            height=player_info['height'],
            weight=player_info['weight'],
            isInjured=player_info['injured'],
            imageUrl=player_info['photo'],
            teamId=stats['team']['id'],
            leagueId=stats['league']['id'],
            fieldPosition=stats['games']['position'],
            isCaptain=stats['games']['captain'],
            goalsTotal=stats['goals']['total'] or 0,
            assists=stats['goals']['assists'] or 0
        )

        football_players.append(football_player)
        download_and_upload_image(football_player)

    # Add player instances to db table
    try:
        football_players_table.put_items(football_players)
    except Exception:
        Logger().exception("Error creating football players list")
