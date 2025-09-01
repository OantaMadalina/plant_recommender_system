import json
from http import HTTPStatus


def test_get_songs_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_get_songs import get_songs_handler
    event = {}
    result = get_songs_handler(event, None)
    songs = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(songs) == 5
    assert songs == [{
        "songId": "sinvseiodoe3412",
        "songName": "Nu ma duc la club",
        "artist": "Theo Rose",
        "YTURL": "https://youtu.be/8KqCvzln7_4?si=ND20o4gopwb1gvFN",
        "locations": []
    }, {
        "songId": "asnufcimi351",
        "songName": "Macarena",
        "artist": "Erika Isac",
        "YTURL": "https://youtu.be/C0Bc0nwSerM?si=9PeP6gGS2yabtlyl",
        "locations": []
    }, {
        "songId": "vsaiofnii5n124",
        "songName": "DNA",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "YTURL": "https://youtu.be/NLZRYQMLDW4?si=QWAixcXKFJnxktgJ",
        "locations": []
    }, {
        "songId": "amcassongIdovmiamer34124",
        "songName": "HUMBLE.",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "YTURL": "https://youtu.be/tvTRZJ-4EyI?si=LBFKuF3p7e32ekhF",
        "locations": []
    }, {
        "songId": "981092491273dwsd",
        "songName": "family ties",
        "artist": "Baby Keem, Kendrick Lamar",
        "YTURL": "https://youtu.be/v6HBZC9pZHQ?si=t1ZYMhYMyOtNHQXf",
        "locations": []
    }]


def test_get_songs_empty_ok(aws_credentials, songs_table):
    from services.music_dashboard.lambda_get_songs import get_songs_handler
    event = {}
    result = get_songs_handler(event, None)
    songs = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(songs) == 0


def test_get_filtered_songs_by_artist_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_get_songs import get_songs_handler
    event = {
        "queryStringParameters": {
            "searchContent": "Kendrick"
        }
    }
    result = get_songs_handler(event, None)
    songs = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(songs) == 3
    assert songs == [{
        "songId": "vsaiofnii5n124",
        "songName": "DNA",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "YTURL": "https://youtu.be/NLZRYQMLDW4?si=QWAixcXKFJnxktgJ",
        "locations": []
    }, {
        "songId": "amcassongIdovmiamer34124",
        "songName": "HUMBLE.",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "YTURL": "https://youtu.be/tvTRZJ-4EyI?si=LBFKuF3p7e32ekhF",
        "locations": []
    }, {
        "songId": "981092491273dwsd",
        "songName": "family ties",
        "artist": "Baby Keem, Kendrick Lamar",
        "YTURL": "https://youtu.be/v6HBZC9pZHQ?si=t1ZYMhYMyOtNHQXf",
        "locations": []
    }]


def test_get_filtered_songs_by_album_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_get_songs import get_songs_handler
    event = {
        "queryStringParameters": {
            "searchContent": "DAMN."
        }
    }
    result = get_songs_handler(event, None)
    songs = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(songs) == 2
    assert songs == [{
        "songId": "vsaiofnii5n124",
        "songName": "DNA",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "YTURL": "https://youtu.be/NLZRYQMLDW4?si=QWAixcXKFJnxktgJ",
        "locations": []
    }, {
        "songId": "amcassongIdovmiamer34124",
        "songName": "HUMBLE.",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "YTURL": "https://youtu.be/tvTRZJ-4EyI?si=LBFKuF3p7e32ekhF",
        "locations": []
    }]


def test_get_filtered_songs_by_song_name_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_get_songs import get_songs_handler
    event = {
        "queryStringParameters": {
            "searchContent": "Nu ma duc la club"
        }
    }
    result = get_songs_handler(event, None)
    songs = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(songs) == 1
    assert songs == [{
        "songId": "sinvseiodoe3412",
        "songName": "Nu ma duc la club",
        "artist": "Theo Rose",
        "YTURL": "https://youtu.be/8KqCvzln7_4?si=ND20o4gopwb1gvFN",
        "locations": []
    }]


def test_get_filtered_songs_no_results_ok(aws_credentials, insert_songs):
    from services.music_dashboard.lambda_get_songs import get_songs_handler
    event = {
        "queryStringParameters": {
            "searchContent": "Puerto Rico"
        }
    }
    result = get_songs_handler(event, None)
    songs = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK.value
    assert len(songs) == 0
