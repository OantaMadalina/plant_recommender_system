from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Attr
# import pandas as pd
import csv

from bootcamp_lib.s3 import CavendishS3

from bootcamp_lib.lambda_middleware import lambda_logger
from services.horoscope.table_horoscope_rating import HoroscopeRatingTable
from services.horoscope.table_horoscope_stats import HoroscopeStatsTable


cav_s3 = CavendishS3('bootcampengine-dev')
dynamodb_res = boto3.resource("dynamodb")
horoscope_rating_table = HoroscopeRatingTable(dynamodb_res)
horoscope_stats_table = HoroscopeStatsTable(dynamodb_res)


def update_horoscope_stats(report_type: str):
    date_format = "%Y-%m-%d"
    key = "latestWeeklyReport"
    if report_type == "monthly":
        date_format = "%B.%Y"
        key = "latestMonthlyReport"
    current_stat = horoscope_stats_table.get_item(
        {"horoscopeStatType": key}, as_dict=True)
    if "Item" in current_stat:
        if datetime.strptime(datetime.now().strftime(date_format), date_format) > datetime.strptime(current_stat["date"], date_format):
            horoscope_stats_table.put_item({"horoscopeStatType": key,
                                            "date": datetime.now().strftime(date_format)})
    else:
        horoscope_stats_table.put_item({"horoscopeStatType": key,
                                        "date": datetime.now().strftime(date_format)})


def _get_start_end_date(report_type):
    current_date = datetime.now()
    if report_type == "weekly":
        start_date = current_date - \
            timedelta(days=current_date.weekday() + 7)  # Previous Monday
        end_date = current_date - timedelta(days=current_date.weekday())
    elif report_type == "monthly":
        prev_month_date = current_date.replace(day=1) - timedelta(days=1)
        start_date = prev_month_date.strftime("%B.%Y")
        end_date = prev_month_date.strftime("%B.%Y")
    return start_date, end_date


def _query_ratings(start_date, end_date, report_type):
    if report_type == 'weekly':
        start_date_str = start_date.strftime("%m.%d.%Y")
        end_date_str = end_date.strftime("%m.%d.%Y")
        response = horoscope_rating_table.scan(filter=(Attr("date").between(
            start_date_str, end_date_str)), as_dict=True)
    elif report_type == 'monthly':
        response = horoscope_rating_table.scan(
            filer=(Attr("date").eq(start_date)), as_dict=True)
    return response


def generate_csv_report(ratings, report_type):
    # df = pd.DataFrame(ratings)
    # for index, row in df.iterrows():
    # row['idRatingMapping'] = row['idRatingMapping'].split("#")[1]
    # df.rename(columns={"idRatingMapping": "sign"})
    # if report_type == "weekly":
    # week_start_str = datetime.strptime(df['date'].min(), "%m.%d.%Y").strftime("%m-%d-%Y")
    # week_end_str = datetime.strptime(df['date'].max(), "%m.%d.%Y").strftime("%m-%d-%Y")
    # csv_report_file = f"{week_start_str}_to_{week_end_str}_report.csv"
    # tmp_csv_file = f"/tmp/{csv_report_file}"
    # elif report_type == "monthly":
    # csv_report_file = f"{ratings[0]['date']}_report.csv"
    # tmp_csv_file = f"/tmp/{csv_report_file}"
    # df.to_csv(tmp_csv_file, index=False)
    dates = [datetime.strptime(rating['date'], "%m.%d.%Y")
             for rating in ratings]
    min_date = min(dates).strftime("%m-%d-%Y")
    max_date = max(dates).strftime("%m-%d-%Y")
    if report_type == "weekly":
        csv_report_file = f"{min_date}_to_{max_date}_report.csv"
    elif report_type == "monthly":
        csv_report_file = f"{min_date}_report.csv"
    tmp_csv_file = f"/tmp/{csv_report_file}"
    for rating in ratings:
        rating['idRatingMapping'] = rating['idRatingMapping'].split("#")[1]
    horoscope_rating_header = {
        "idRatingMapping": "Sign", "date": "Date", "rating": "Rating"}
    with open(tmp_csv_file, mode="w", newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=["idRatingMapping", "date", "rating"])
        writer.writerow(horoscope_rating_header)
        writer.writerows(ratings)
    return tmp_csv_file, csv_report_file


@lambda_logger(log_input=True)
def horoscope_rating_report_handler(event, _):
    report_type = event.get("type")

    start_date, end_date = _get_start_end_date(report_type)
    ratings = _query_ratings(start_date, end_date, report_type)
    tmp_csv_file, csv_report_file = generate_csv_report(ratings, report_type)
    cav_s3.upload_file(tmp_csv_file, f'Horoscope/Report/{csv_report_file}')
    update_horoscope_stats(report_type)
