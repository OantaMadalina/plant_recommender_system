from http import HTTPStatus
import os
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, BadRequestException
)
from bootcamp_lib.logger import Logger
from services.music_dashboard.table_songs import SongsTable
from services.music_dashboard.utils import create_presigned_get, get_item
from services.music_dashboard.responses import SongResponse


@http_request()
def get_song_locations_handler(request: HttpRequestData, _):

    songId = request.pathParams.get("songId", None)
    if not songId:
        raise BadRequestException("Invalid path parameters!")

    try:
        song = get_item({"songId": songId},
                        SongsTable,
                        projection="songId,YTURL,locations",
                        as_dict=True)

        if not song or not song.get("Item"):
            return (HTTPStatus.NOT_FOUND,
                    SongResponse(songId, "The song could not be found!").to_dict())

        song["Item"]["locations"] = [
            {**location,
             "imagePath": create_presigned_get(os.environ["BOOTCAMP_BUCKET"],
                                               location["imagePath"])}
            for location in song["Item"]["locations"]
        ]

        return song["Item"]

    except Exception as ex:
        Logger().error(str(ex))
        return (HTTPStatus.INTERNAL_SERVER_ERROR,
                SongResponse(_, "The song's locations could not be fetched").to_dict())
