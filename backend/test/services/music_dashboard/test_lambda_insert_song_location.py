import boto3
import json
import os

from http import HTTPStatus
from boto3.dynamodb.conditions import Key


def bucket_file_exists(bucket, file):
    s3 = boto3.resource("s3")
    return any(
        obj.bucket_name == bucket and obj.key == file
        for obj in s3.Bucket(os.environ["BOOTCAMP_BUCKET"]).objects.all())


def get_song_locations(song_id):
    return boto3.resource("dynamodb").Table("bootcampengine_test_songs").query(
        KeyConditionExpression=Key("songId").eq(song_id)).get("Items")


def put_song(song):
    boto3.resource("dynamodb").Table("bootcampengine_test_songs-locations").put_item(Item=song)


def test_insert_song_location_ok(aws_credentials, insert_songs, insert_song_locations, bootcamp_bucket):
    from services.music_dashboard.lambda_insert_song_location import insert_song_location_handler
    event = {
        "body": json.dumps({
            "songId": "sinvseiodoe3412",
            "locationId": "43642g",
            "imagePath": "some/path/to/s3"
        })
    }
    result = insert_song_location_handler(event, None)

    assert result["statusCode"] == HTTPStatus.OK.value

    response = json.loads(result["body"])
    assert response["message"] == "The song location was successfully inserted!"

    song_locations = get_song_locations("sinvseiodoe3412")[0]["locations"]
    assert len(song_locations) == 3


def test_insert_song_location_invalid_song_id_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_insert_song_location import insert_song_location_handler
    event = {
        "body": json.dumps({
            "songId": ""
        })
    }
    result = insert_song_location_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'songId' is required"


def test_insert_song_invalid_song_image_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_insert_song_location import insert_song_location_handler
    event = {
        "body": json.dumps({
            "songId": "numaduclaclub##",
            "imagePath": ""
        })
    }
    result = insert_song_location_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'imagePath' is required"


def test_insert_song_location_empty_body_fail(aws_credentials, insert_songs, insert_song_locations):
    from services.music_dashboard.lambda_insert_song_location import insert_song_location_handler
    event = {
        "body": json.dumps({})
    }
    result = insert_song_location_handler(event, None)
    assert result["statusCode"] == HTTPStatus.BAD_REQUEST.value
    response = json.loads(result["body"])
    assert response["error"] == "Body field 'songId' is required"
