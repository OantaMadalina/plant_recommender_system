import os
import requests
import base64
from bootcamp_lib.lambda_middleware import (HttpRequestData, http_request, BadRequestException,
                                            InternalServerErrorException)
from bootcamp_lib.logger import Logger
from bootcamp_lib.s3 import CavendishS3
from services.music_dashboard.utils import create_presigned_post


cav_s3 = CavendishS3(os.environ["BOOTCAMP_BUCKET"])


def upload_image(data: str, filename: str):
    s3_key = f"MusicDashboard/Locations/Images/{filename}"
    signed_url = create_presigned_post(os.environ["BOOTCAMP_BUCKET"], s3_key)

    index = data.find("base64,")

    if index != -1:
        data = data[index + len("base64,"):]

    local_file_path = f"/tmp/{filename}"
    try:
        with open(local_file_path, "wb") as fh:
            fh.write(base64.b64decode(data))
        with open(local_file_path, "rb") as fw:
            files = {'file': (s3_key, fw)}
            http_response = requests.post(signed_url["url"], data=signed_url["fields"], files=files)

        os.remove(local_file_path)

        Logger().info(f'File upload HTTP status code: {http_response.status_code}')

        return s3_key
    except Exception as ex:
        raise ex


@http_request(
    request_type="PUT",
    content_type="text/plain"
)
def upload_location_image_handler(request: HttpRequestData, _):

    filename = request.pathParams.get("filename")

    if not filename:
        raise BadRequestException("Invalid filename parameter.")

    try:
        return upload_image(request.body, filename)
    except Exception as ex:
        raise InternalServerErrorException(f"The image could not be uploaded: {ex}")
