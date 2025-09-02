from botocore.exceptions import ClientError
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, BadRequestException,
    HTTPStatus
)
from bootcamp_lib.logger import (
    Logger
)
from services.music_dashboard.table_songs import SongsTable
from services.music_dashboard.responses import SongResponse
from services.music_dashboard.utils import remove_item


@http_request(
    request_type="DELETE"
)
def remove_song_handler(request: HttpRequestData, _):
    if not request.pathParams.get("songId", ""):
        raise BadRequestException("Invalid request path parameters!")

    try:
        remove_item(request.pathParams,
                    SongsTable,
                    condition_expression="attribute_exists(songId)")
        http_status = HTTPStatus.OK
        message = "The song was successfully removed!"
    except ClientError as ex:
        http_status = HTTPStatus.NOT_FOUND
        message = "The song could not be found!"
        Logger().error(str(ex))
    except Exception as ex:
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        message = "The song could not be removed!"
        Logger().error(str(ex))
    finally:
        return http_status, SongResponse(request.pathParams["songId"], message).to_dict()
