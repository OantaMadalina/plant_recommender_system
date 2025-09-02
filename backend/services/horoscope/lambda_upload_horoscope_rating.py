from datetime import datetime
import boto3
import random
import string
from botocore.exceptions import ClientError

from services.horoscope.table_horoscope_rating import HoroscopeRatingTable
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException
)

signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
         'capricorn', 'aquarius', 'pisces', '']


dynamodb_res = boto3.resource("dynamodb")
horoscope_rating_table = HoroscopeRatingTable(dynamodb_res)


def _id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@http_request()
def horoscope_upload_rating_handler(request: HttpRequestData, context):

    sign = request.queryParams.get("sign", "")
    type = request.queryParams.get("type", "")
    rating = request.queryParams.get("rating", "")

    if sign.lower() not in signs:
        raise BadRequestException("Sign not found.")
    if type.lower() not in ['daily', 'monthly', '']:
        raise BadRequestException("Horoscope type has to be 'daily' or 'monthly'.")
    if not rating or not rating.isnumeric():
        raise BadRequestException("Review is required and has to be a number.")
    id = _id_generator()
    current_date = datetime.now()
    if type.lower() == 'daily':
        query_date = current_date.strftime("%m.%d.%Y")
    elif type.lower() == 'monthly':
        query_date = current_date.strftime("%B.%Y")
    key = f'{id}#{sign.title()}#{query_date}'
    try:
        horoscope_rating_table.put_item(item={"idRatingMapping": key, "rating": rating,
                                              "date": query_date})
    except ClientError:
        return "Could not add rating."
