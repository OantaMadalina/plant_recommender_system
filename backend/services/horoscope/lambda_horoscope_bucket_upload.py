from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException
)
from bootcamp_lib.s3 import CavendishS3

cav_s3 = CavendishS3('bootcampengine-dev')


@http_request(
    content_type="application/octet"
)
def horoscope_bucket_upload_handler(request: HttpRequestData, _):
    filename = request.pathParams.get("filename")

    if not filename.endswith('.csv'):
        raise BadRequestException("File type unsupported")

    file = "/tmp/{}".format(filename)

    with open(file, "w") as f:
        f.write(request.body)

    cav_s3.upload_file(file, f'Horoscope/Data/{filename}')
