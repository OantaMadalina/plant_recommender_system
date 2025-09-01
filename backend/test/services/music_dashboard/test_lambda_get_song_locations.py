import json
from http import HTTPStatus


def test_get_song_locations_ok(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_get_song_locations import get_song_locations_handler
    event = {
        "pathParameters": {
            "songId": "sinvseiodoe3412"
        }
    }
    result = get_song_locations_handler(event, None)
    song = json.loads(result["body"])
    locations = song["locations"]
    assert song.get("artist") is None
    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(locations) == 2


def test_get_song_locations_missing_songId_fail(aws_credentials, songs_table):
    from services.music_dashboard.lambda_get_song_locations import get_song_locations_handler
    event = {
        "pathParameters": {
            "songId": ""
        }
    }

    result = get_song_locations_handler(event, None)

    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])

    assert response["error"] == "Invalid path parameters!"


def test_get_song_location_not_found_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_get_song_locations import get_song_locations_handler
    event = {
        "pathParameters": {
            "songId": "sinvseiodoe34"
        }
    }
    result = get_song_locations_handler(event, None)
    response = json.loads(result["body"])
    assert result["statusCode"] == HTTPStatus.NOT_FOUND.value
    assert response["message"] == "The song could not be found!"
