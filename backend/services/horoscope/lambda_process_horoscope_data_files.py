import csv
import os
from datetime import datetime
from dateutil import parser

import boto3
from botocore.exceptions import ClientError

from bootcamp_lib.lambda_middleware import lambda_logger, ErrorException
from bootcamp_lib.logger import Logger
from services.horoscope.table_horoscope_data import HoroscopeDataTable
from services.horoscope.table_horoscope_stats import HoroscopeStatsTable
from bootcamp_lib.s3 import CavendishS3

dynamodb_res = boto3.resource("dynamodb")
horoscope_table = HoroscopeDataTable(dynamodb_res)
horoscope_stats_table = HoroscopeStatsTable(dynamodb_res)
cav_s3 = CavendishS3('bootcampengine-dev')


def update_horoscope_stats(entries: list, date_format: str):
    key = "latestWeeklyPrediction"
    if date_format == "%B.%Y":
        key = "latestMonthlyPrediction"
    current_stat = horoscope_stats_table.get_item(
        {"horoscopeStatType": key}, as_dict=True)
    date_objects = map(lambda entry: datetime.strptime(
        entry["horoscopeDate"], date_format), entries)
    highest_date = max(date_objects)
    if "Item" in current_stat:
        current_stat_date = datetime.strptime(
            current_stat["date"], date_format)
        if highest_date > current_stat_date:
            Logger().info(
                f"Will update stat for {key} to date {highest_date.strftime(date_format)}")
            horoscope_stats_table.put_item(
                {"horoscopeStatType": key, "date": highest_date.strftime(date_format)})
    else:
        horoscope_stats_table.put_item(
            {"horoscopeStatType": key, "date": highest_date.strftime(date_format)})


def verify_horoscope_entry(entry: dict):
    """Returns True if entry does not exists in DynamoDB or shows differences, False if not"""
    key = f"{entry['sign']}#{entry['horoscopeDate']}"
    result = horoscope_table.get_item({"signDateMapping": key}, as_dict=True)
    if "Item" not in result:
        return True, key
    else:
        if entry["horoscopeString"] != result["Item"]["horoscopeString"]:
            Logger().info("Will update entry {key}")
            return True, key
        return False, key


def process_horoscope_data_file(filename):
    fields = ["sign", "horoscopeDate", "horoscopeString"]

    entries = []
    with open(filename) as data_file:
        lines = data_file.readlines()
        while lines:
            reader = csv.DictReader(lines, fieldnames=fields)
            for row in reader:
                entries.append(row)
            break
    results = []
    for entry in entries:
        parsed_date = parser.parse(entry["horoscopeDate"])
        date_format = "%Y-%m-%d"
        if entry["horoscopeDate"].count(".") == 1 or entry["horoscopeDate"].count("-") == 1:
            date_format = "%B.%Y"
        entry["horoscopeDate"] = parsed_date.strftime(date_format)
        entry["sign"] = entry["sign"].lower()
        add_entry, add_key = verify_horoscope_entry(entry)
        if add_entry:
            entry["signDateMapping"] = add_key
            results.append(entry)

    Logger().info("Adding entries to table")
    for result in results:
        horoscope_table.put_item(result)

    update_horoscope_stats(entries, date_format)


def download_data_file(filename: str) -> str:
    try:
        os.mkdir("/tmp/bootcamp_tmp")
    except FileExistsError:
        pass

    tmp_filename = os.path.join(
        "/tmp/bootcamp_tmp/", os.path.basename(filename))

    try:
        cav_s3.download_file(filename, tmp_filename)
    except ClientError as e:
        if e.response["Error"]["Code"] != "404":
            raise

    bucket_path = os.path.dirname(
        filename) + "/" + os.path.basename(tmp_filename)
    return tmp_filename, bucket_path


@lambda_logger(log_input=True)
def process_horoscope_data_file_handler(event, _):
    filename = event["Records"][0]["s3"]["object"]["key"]

    if "/Processed/" in filename:
        return

    try:
        filename, s3_filename = download_data_file(filename)
    except Exception as e:
        raise ErrorException(e)

    try:
        process_horoscope_data_file(filename)
    finally:
        try:
            os.remove(filename)
        except Exception:
            Logger().exception(f"Error removing {filename}")

        cav_s3.archive_file(s3_filename)
