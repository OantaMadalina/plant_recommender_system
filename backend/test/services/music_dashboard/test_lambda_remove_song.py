import json
import boto3
from http import HTTPStatus


def get_song_by_id(songId):
    return boto3.resource("dynamodb").Table("bootcampengine_test_songs").get_item(
        Key={"songId": songId}).get("Item")


def test_remove_song_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_remove_song import remove_song_handler
    event = {
        "pathParameters": {
            "songId": "vsaiofnii5n124"
        }
    }
    result = remove_song_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK.value

    response = json.loads(result["body"])

    assert response["message"] == "The song was successfully removed!"
    assert response["songId"] == "vsaiofnii5n124"
    song = get_song_by_id("vsaiofnii5n124")
    assert song is None


def test_remove_song_song_not_found_fail(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_remove_song import remove_song_handler

    event = {
        "pathParameters": {
            "songId": "sth"
        },
    }
    result = remove_song_handler(event, None)
    assert result["statusCode"] == HTTPStatus.NOT_FOUND.value
    response = json.loads(result["body"])
    assert response["message"] == "The song could not be found!"


def test_remove_song_invalid_song_id_fail(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_remove_song import remove_song_handler

    event = {
        "pathParameters": {},
    }
    result = remove_song_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Invalid request path parameters!"
