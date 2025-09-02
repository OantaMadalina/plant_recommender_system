from boto3.dynamodb.conditions import Attr

from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, HTTPStatus
)
from bootcamp_lib.logger import Logger

from services.music_dashboard.table_songs import SongsTable
from services.music_dashboard.responses import SongResponse
from services.music_dashboard.utils import scan_table


@http_request()
def get_songs_handler(request: HttpRequestData, _):
    try:
        search_content = request.queryParams.get("searchContent", None)
        scan_filter = (Attr("searchToken").contains(search_content.lower().replace(' ', ''))
                       if search_content else search_content)
        return scan_table(SongsTable, filter=scan_filter,
                          projection="songId,songName,artist,album,YTURL,locations", as_dict=True)
    except Exception as ex:
        Logger().error(str(ex))
        return (HTTPStatus.INTERNAL_SERVER_ERROR,
                SongResponse(_, "The songs could not be fetched").to_dict())
