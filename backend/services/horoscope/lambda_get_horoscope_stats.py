import boto3
import re
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData,
)
from services.horoscope.table_horoscope_stats import HoroscopeStatsTable
from bootcamp_lib.s3 import CavendishS3

dynamodb_res = boto3.resource("dynamodb")
horoscope_stats = HoroscopeStatsTable(dynamodb_res)
cav_s3 = CavendishS3('bootcampengine-dev')


@http_request
def get_horoscope_stats_handler(request: HttpRequestData, context):
    response = []
    results = horoscope_stats.scan(as_dict=True)
    for result in results:
        list_result = list(result.values())
        list_result[0] = list_result[0].replace('latest', 'Latest')
        list_result[0] = ' '.join(re.findall('[A-Z][^A-Z]*', list_result[0]))
        response.append(' - '.join(list_result))
    return response
