import os
from dacite import from_dict
from http import HTTPStatus

from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request
)
from bootcamp_lib.logger import Logger

from services.music_dashboard.table_songs import (
    SongLocationModel, SongsTable
)
from services.music_dashboard.responses import SongLocationResponse
from services.music_dashboard.utils import create_presigned_get, update_item


@http_request(
    request_type="POST",
    validation={
        "songId": {"required": True},
        "imagePath": {"required": True}
    }
)
def insert_song_location_handler(request: HttpRequestData, _):

    try:
        song_id = request.dictBody["songId"]
        song_location = from_dict(SongLocationModel, request.dictBody)

        update_item({"songId": song_id},
                    SongsTable,
                    update_expression="SET locations = list_append(locations, :l)",
                    expression_attribute_values={
                        ":l": [song_location.to_dict()]
                    })

        http_status = HTTPStatus.OK
        message = "The song location was successfully inserted!"
    except Exception as ex:
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        message = "The song location could not be inserted!"
        Logger().error(str(ex))
    finally:
        body = SongLocationResponse(songId=song_id,
                                    message=message,
                                    location={
                                        **song_location.to_dict(),
                                        "imagePath": create_presigned_get(
                                            os.environ["BOOTCAMP_BUCKET"],
                                            song_location.imagePath) or ''
                                    }).to_dict()

        return http_status, body
