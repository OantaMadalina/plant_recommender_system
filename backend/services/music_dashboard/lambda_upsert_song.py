from dacite import from_dict

from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, HTTPStatus
)
from bootcamp_lib.logger import Logger

from services.music_dashboard.table_songs import (
    SongLocationModel, SongsTable, SongModel
)
from services.music_dashboard.responses import SongResponse
from services.music_dashboard.utils import put_item


def generate_search_token(song_data: dict[str, str]) -> str:
    search_token = (f"{song_data.get('songName','').replace(' ','').lower()}#"
                    f"{song_data.get('artist','').replace(' ','').lower()}#"
                    f"{song_data.get('album','').replace(' ','').lower()}")
    return search_token


@http_request(
    request_type="POST",
    validation={
        "songName": {"required": True},
        "artist": {"required": True},
        "YTURL": {"required": True}
    }
)
def upsert_song_handler(request: HttpRequestData, _):

    dictBody = request.dictBody

    formatted_yt_url = (dictBody["YTURL"].strip()
                        .replace("/watch?v=", "/embed/")
                        .replace("/youtu.be/", "/www.youtube.com/embed/"))
    # Strip strings
    dictBody.update({"songName": dictBody["songName"].strip(),
                     "artist": dictBody["artist"].strip(),
                     "album": dictBody.get("album", "").strip(),
                     "YTURL": formatted_yt_url,
                     "locations": [from_dict(SongLocationModel, location)
                                   for location in dictBody["locations"]]
                     })

    # Generate the search token based on the data inserted by the user
    search_token = generate_search_token(dictBody)
    if search_token != dictBody.get("searchToken", ""):
        dictBody.update({"searchToken": search_token})

    try:
        song = from_dict(SongModel, dictBody)

        put_item(song, SongsTable)

        http_status = HTTPStatus.OK
        message = "The song was successfully upserted!"
    except Exception as ex:
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        message = "The song could not be upserted!"
        Logger().error(str(ex))
    finally:
        return http_status, SongResponse(song.songId, message).to_dict()
