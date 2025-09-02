from http import HTTPStatus

from botocore.exceptions import ClientError

from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, BadRequestException
)
from bootcamp_lib.logger import Logger

from services.music_dashboard.table_songs import SongsTable
from services.music_dashboard.responses import SongLocationResponse
from services.music_dashboard.utils import update_item, get_item


@http_request(
    request_type="DELETE"
)
def remove_song_location_handler(request: HttpRequestData, _):
    if not request.pathParams.get("songId", "") or not request.pathParams.get("locationId", ""):
        raise BadRequestException("Invalid request path parameters!")

    try:
        song_id = request.pathParams["songId"]
        item_key = {"songId": song_id}
        location_id = request.pathParams["locationId"]

        song = get_item(item_key,
                        SongsTable,
                        projection="locations")

        locations = song.to_dict()["locations"] if song else None

        if not locations:
            http_status = HTTPStatus.NOT_FOUND
            message = "The song location could not be found!"
            return

        filtered_locations = list(filter(lambda x: x["locationId"] != location_id, locations))

        update_item(item_key,
                    SongsTable,
                    update_expression="SET locations = :i",
                    expression_attribute_values={
                        ":i": filtered_locations
                    })

        http_status = HTTPStatus.OK
        message = "The song location was successfully removed!"

    except ClientError as ex:
        http_status = HTTPStatus.NOT_FOUND
        message = "The song location could not be found!"
        Logger().error(str(ex))

    except Exception as ex:
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        message = "The song location could not be removed!"
        Logger().error(str(ex))

    finally:
        body = SongLocationResponse(songId=request.pathParams["songId"],
                                    location={"locationId": request.pathParams["locationId"]},
                                    message=message).to_dict()
        return http_status, body
