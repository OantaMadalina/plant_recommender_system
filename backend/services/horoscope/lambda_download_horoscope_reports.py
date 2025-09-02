import boto3
import json
import re
from dateutil import parser

from services.horoscope.table_horoscope_stats import HoroscopeStatsTable
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException, InternalServerErrorException
)

dynamodb_res = boto3.resource("dynamodb")
horoscope_stats_table = HoroscopeStatsTable(dynamodb_res)
bucket_name = "bootcampengine-dev"
prefix = 'Horoscope/Report'
s3_client = boto3.client("s3")


@http_request()
def download_horoscope_reports_handler(request: HttpRequestData, context):
    type = request.queryParams.get("type", "")

    pattern = r"(0[1-9]|1[1,2])-(0[1-9]|[12][0-9]|3[01])-(19|20)\d{2}"

    if type.lower() not in ['weekly', 'monthly']:
        return {'statusCode': 404,
                'body': json.dumps({'error': 'No files found in S3.'})}

    latest_report_type = "latestWeeklyReport" if type == "weekly" else "latestMonthlyReport"
    # date_format = "%Y-%m-%d" if type == "weekly" else "%B.%Y"
    latest_report = horoscope_stats_table.get_item(
        {"horoscopeStatType": latest_report_type}, as_dict=True)
    if 'Item' not in latest_report:
        latest_report_date = None
    else:
        latest_report_date = latest_report['Item']['date']
        latest_parsed_date = parser.parse(latest_report_date)

    try:
        s3_reports = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=prefix)
        latest_file = None
        if 'Contents' in s3_reports:
            for report in s3_reports['Contents']:
                report_date = report['LastModified'].replace(
                    hour=0, minutes=0, second=0, microsecond=0)
                if report_date == latest_parsed_date:
                    if type == 'weekly' and len(re.findall(pattern, report['Key'])) == 2:
                        latest_file = report['Key']
                        break
                    if type == 'monthly' and len(re.findall(pattern, report['Key'])) == 1:
                        latest_file = report['Key']
                        break
            return {'statusCode': 404,
                    'body': json.dumps({'error': 'Could not get any data.'})}
        if latest_file:
            file_path = f"/tmp/bootcamp_tmp/{latest_file.split('/')[-1]})"
            s3_client.download_file(bucket_name, latest_file, file_path)
            return {'statusCode': 200,
                    'body': json.dumps({'filePath': file_path})}
        else:
            return {'statusCode': 404,
                    'body': json.dumps({'error': 'No files found in S3.'})}
    except Exception as e:
        raise InternalServerErrorException(str(e))
