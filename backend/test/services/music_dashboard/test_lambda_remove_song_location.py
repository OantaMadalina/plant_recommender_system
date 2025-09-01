import json
import boto3
from http import HTTPStatus

BOOTCAMP_BUCKET = "test"


def get_song_location(key_dict: dict):
    return boto3.resource("dynamodb").Table("bootcampengine_test_songs").get_item(
        Key=key_dict, ProjectionExpression="locations")["Item"]


def test_remove_song_location_ok(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_remove_song_location import remove_song_location_handler
    event = {
        "pathParameters": {
            "songId": "vsaiofnii5n124",
            "locationId": "12412432dvci"
        }
    }
    result = remove_song_location_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK.value
    response = json.loads(result["body"])

    assert response["message"] == "The song location was successfully removed!"
    assert response["location"]["locationId"] == "12412432dvci"

    song = get_song_location({
        "songId": "vsaiofnii5n124"
    })
    assert len(song["locations"]) == 0


def test_remove_song_location_not_found_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_remove_song_location import remove_song_location_handler

    event = {
        "pathParameters": {
            "songId": "sth",
            "locationId": "sthelse"
        },
    }
    result = remove_song_location_handler(event, None)
    assert result["statusCode"] == HTTPStatus.NOT_FOUND.value
    response = json.loads(result["body"])
    assert response["message"] == "The song location could not be found!"


def test_remove_song_location_invalid_song_id_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_remove_song_location import remove_song_location_handler

    event = {
        "pathParameters": {
            "locationId": "djvfidsg"
        },
    }
    result = remove_song_location_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Invalid request path parameters!"


def test_remove_song_location_invalid_location_id_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_remove_song_location import remove_song_location_handler

    event = {
        "pathParameters": {
            "songId": "oirgmvi3",
            "locationId": ""
        },
    }
    result = remove_song_location_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Invalid request path parameters!"
