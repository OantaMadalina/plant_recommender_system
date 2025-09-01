import boto3
import json

from boto3.dynamodb.conditions import Key
from http import HTTPStatus


def get_song_by_search_token(search_token):
    return boto3.resource("dynamodb").Table("bootcampengine_test_songs").query(
        IndexName="searchToken-index",
        KeyConditionExpression=Key("searchToken").eq(search_token)).get("Items")[0]


def get_song_by_id(songId):
    return boto3.resource("dynamodb").Table("bootcampengine_test_songs").get_item(
        Key={"songId": songId}).get("Item")


def put_song(song):
    boto3.resource("dynamodb").Table("bootcampengine_test_songs").put_item(Item=song)


def test_update_song_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songId": "sinvseiodoe3412",
            "songName": "Ba ma duc la club!",
            "artist": "Theo R",
            "YTURL": "https://youtu.be/"
        })
    }
    result = upsert_song_handler(event, None)

    response = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert response["message"] == "The song was successfully upserted!"
    assert response["songId"] == "sinvseiodoe3412"

    song = get_song_by_id("sinvseiodoe3412")
    assert {
        "songId": "sinvseiodoe3412",
        "songName": "Ba ma duc la club!",
        "artist": "Theo R",
        "searchToken": "bamaduclaclub!#theor#",
        "YTURL": "https://www.youtube.com/embed/",
        "locations": []
    } == song


def test_insert_song_share_url_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songName": " 8IULIE FREESTYLE ",
            "artist": "   Stefan Costea ",
            "YTURL": "https://youtu.be/DzzQTCnwbPk?si=XD-f47ha0SFhp-Cv"
        })
    }
    result = upsert_song_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK.value

    response = json.loads(result["body"])

    assert response["message"] == "The song was successfully upserted!"
    song = get_song_by_search_token("8iuliefreestyle#stefancostea#")
    assert {
        "songName": "8IULIE FREESTYLE",
        "artist": "Stefan Costea",
        "searchToken": "8iuliefreestyle#stefancostea#",
        "YTURL": "https://www.youtube.com/embed/DzzQTCnwbPk?si=XD-f47ha0SFhp-Cv",
        "locations": []

    }.items() <= song.items()


def test_insert_song_basic_url_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songName": " flawless ",
            "artist": "   Zelthya ",
            "YTURL": "https://www.youtube.com/watch?v=W9DeZwznxlo"
        })
    }
    result = upsert_song_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK.value

    response = json.loads(result["body"])

    assert response["message"] == "The song was successfully upserted!"
    song = get_song_by_search_token("flawless#zelthya#")
    assert {
        "songName": "flawless",
        "artist": "Zelthya",
        "searchToken": "flawless#zelthya#",
        "YTURL": "https://www.youtube.com/embed/W9DeZwznxlo",
        "locations": []

    }.items() <= song.items()


def test_insert_song_embed_url_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songName": " flawless ",
            "artist": "   Zelthya ",
            "YTURL": "https://www.youtube.com/embed/W9DeZwznxlo?si=zi8twZRWjJjmNHKB"
        })
    }
    result = upsert_song_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK.value

    response = json.loads(result["body"])

    assert response["message"] == "The song was successfully upserted!"
    song = get_song_by_search_token("flawless#zelthya#")
    assert {
        "songName": "flawless",
        "artist": "Zelthya",
        "searchToken": "flawless#zelthya#",
        "YTURL": "https://www.youtube.com/embed/W9DeZwznxlo?si=zi8twZRWjJjmNHKB",
        "locations": []

    }.items() <= song.items()


def test_upsert_song_invalid_song_name_fail(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songName": "",
            "artist": "Theo Rose",
            "YTURL": "https://youtu.be/8KqCvzln7_4?si=ND20o4gopwb1gvFN"
        })
    }
    result = upsert_song_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'songName' is required"


def test_upsert_song_invalid_song_artist_fail(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songName": "Nu ma duc la club",
            "artist": "",
            "YTURL": "https://youtu.be/8KqCvzln7_4?si=ND20o4gopwb1gvFN"
        })
    }
    result = upsert_song_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'artist' is required"


def test_upsert_song_invalid_song_yt_url_fail(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({
            "songName": "Nu ma duc la club",
            "artist": "Theo Rose",
            "YTURL": ""
        })
    }
    result = upsert_song_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'YTURL' is required"


def test_upsert_song_empty_body_fail(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_upsert_song import upsert_song_handler
    event = {
        "body": json.dumps({})
    }
    result = upsert_song_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'songName' is required"
