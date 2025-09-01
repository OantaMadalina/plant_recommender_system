import os
import boto3

import pytest


def put_song(song):
    boto3.resource("dynamodb").Table("bootcampengine_test_songs").put_item(Item=song)


def put_song_location(location_key, song_locations):
    (boto3.resource("dynamodb")
     .Table("bootcampengine_test_songs")
     .update_item(Key=location_key,
                  UpdateExpression="SET locations = list_append(locations, :l)",
                  ExpressionAttributeValues={
                      ":l": song_locations
                      }))


@pytest.fixture(scope="module")
def aws_credentials():
    os.environ["environment"] = "bootcampengine_test_"
    os.environ["aws_account_id"] = "123456789012"
    os.environ["AWS_REGION"] = "eu-west-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["BOOTCAMP_BUCKET"] = "test"


@pytest.fixture(scope="function")
def songs_table(dynamodb):
    dynamodb.create_table(
        TableName="bootcampengine_test_songs",
        AttributeDefinitions=[
            {
                "AttributeName": "songId",
                "AttributeType": "S"
            },
            {
                "AttributeName": "searchToken",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "songId",
                "KeyType": "HASH"
            }
        ],
        GlobalSecondaryIndexes=[{
            "IndexName": "searchToken-index",
            "KeySchema": [
                {
                    "AttributeName": "searchToken",
                    "KeyType": "HASH"
                }
            ],
            "Projection": {
                "ProjectionType": "ALL"
            },
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10
            }
        }],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )
    yield


@pytest.fixture(scope="function")
def insert_songs(songs_table):
    songs = [{
        "songId": "sinvseiodoe3412",
        "songName": "Nu ma duc la club",
        "artist": "Theo Rose",
        "searchToken": "numaduclaclub#theorose#",
        "YTURL": "https://youtu.be/8KqCvzln7_4?si=ND20o4gopwb1gvFN",
        "locations": []
    }, {
        "songId": "asnufcimi351",
        "songName": "Macarena",
        "artist": "Erika Isac",
        "searchToken": "macarena#erikaisac#",
        "YTURL": "https://youtu.be/C0Bc0nwSerM?si=9PeP6gGS2yabtlyl",
        "locations": []
    }, {
        "songId": "vsaiofnii5n124",
        "songName": "DNA",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "searchToken": "dna#kendricklamar#damn.",
        "YTURL": "https://youtu.be/NLZRYQMLDW4?si=QWAixcXKFJnxktgJ",
        "locations": []

    }, {
        "songId": "amcassongIdovmiamer34124",
        "songName": "HUMBLE.",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "searchToken": "humble.#kendricklamar#damn.",
        "YTURL": "https://youtu.be/tvTRZJ-4EyI?si=LBFKuF3p7e32ekhF",
        "locations": []

    }, {
        "songId": "981092491273dwsd",
        "songName": "family ties",
        "artist": "Baby Keem, Kendrick Lamar",
        "searchToken": "familyties#babykeem,kendricklamar#",
        "YTURL": "https://youtu.be/v6HBZC9pZHQ?si=t1ZYMhYMyOtNHQXf",
        "locations": []

    }]

    for song in songs:
        put_song(song)


@pytest.fixture(scope="function")
def insert_song_locations(songs_table):
    songs = [{
        "songId": "sinvseiodoe3412",
        "locations": [{
            "locationId": "sfiviori4io41",
            "imagePath": "base64code",
            "description": "Sunset in Madeira",
            "latitude": "41.124321",
            "longitude": "12.125421"
            }]
    }, {
        "songId": "sinvseiodoe3412",
        "locations": [{
            "locationId": "mivmfiviowe5",
            "imagePath": "base64code",
            "description": "City break in Bucharest",
            "latitude": "41.124321",
            "longitude": "12.125421"
            }]
    }, {
        "songId": "vsaiofnii5n124",
        "locations": [{
            "locationId": "12412432dvci",
            "imagePath": "base64code",
            "description": "Somewhere nice",
            "latitude": "41.124321",
            "longitude": "12.125421"
            }]
    }, {
        "songId": "amcassongIdovmiamer34124",
        "locations": [{
            "locationId": "dsoicoiowenir3",
            "imagePath": "base64code",
            "description": "WAAWAAAWEEWAA",
            "latitude": "41.124321",
            "longitude": "12.125421"
            }]
    }, {
        "songId": "981092491273dwsd",
        "locations": [{
            "locationId": "12412332kmfas",
            "imagePath": "base64code",
            "description": "Feeling chilly in Italy",
            "latitude": "41.124321",
            "longitude": "12.125421"
            }]
    }]

    for song in songs:
        put_song_location(song, song["locations"])
