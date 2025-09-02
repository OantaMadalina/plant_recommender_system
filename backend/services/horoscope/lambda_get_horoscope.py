from datetime import datetime
import boto3
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData,
    BadRequestException
)
from services.horoscope.table_horoscope_data import HoroscopeDataTable
from bootcamp_lib.s3 import CavendishS3

dynamodb_res = boto3.resource("dynamodb")
horoscope_table = HoroscopeDataTable(dynamodb_res)
cav_s3 = CavendishS3('bootcampengine-dev')

signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
         'capricorn', 'aquarius', 'pisces', '']


def _get_horoscope(sign, type):
    current_date = datetime.now()
    if type.lower() == 'daily':
        query_date = current_date.strftime("%Y-%m-%d")
    elif type.lower() == 'monthly':
        query_date = current_date.strftime("%B.%Y")

    key = f'{sign}#{query_date}'
    result = horoscope_table.get_item({"signDateMapping": key}, as_dict=True)
    if "Item" not in result:
        return "Horoscope does not exists for this sign and prediction"
    else:
        return result['Item']['horoscopeString']


@http_request
def get_horoscope_handler(request: HttpRequestData, context):

    sign = request.queryParams.get("sign", "")
    type = request.queryParams.get("type", "")

    if sign.lower() not in signs:
        raise BadRequestException("Sign not found")
    if type.lower() not in ['daily', 'monthly', '']:
        raise BadRequestException("Horoscope type has to be 'daily' or 'monthly")
    if sign == '' or type == '':
        return "Select a sign as well a prediction type"
    return _get_horoscope(sign, type)
