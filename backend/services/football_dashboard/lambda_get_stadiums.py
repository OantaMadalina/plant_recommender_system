from dataclasses import dataclass
from logging import Logger
import os
from typing import List
from boto3.dynamodb.conditions import Attr
import boto3

from bootcamp_lib.lambda_middleware import BadRequestException, HttpRequestData, http_request
from services.football_dashboard.utils import generate_signed_url
from services.football_dashboard.table_stadiums import StadiumModel, StadiumsTable

dynamodb_res = boto3.resource("dynamodb", verify=False)


@dataclass
class StadiumResponse:
    stadium: StadiumModel
    signedPhotoUrl: str


@dataclass
class StadiumsResponse:
    count: int
    allItems: bool
    items: list[StadiumResponse]
    sizeLimit: int


def format_query_name(name):
    if not name.isalpha():
        raise BadRequestException("Name must contain only alphabetic characters.")

    return ' '.join(word.capitalize() for word in name.lower().split(' '))


def generate_stadiums_response(items: List[StadiumModel], results):
    for item in items:
        try:
            s3_key = (
                "FootballDashboard/StadiumsImages/"
                f"{item.stadiumName.replace(' ', '')}.png"
            )
            signed_url = generate_signed_url(os.environ["BOOTCAMP_BUCKET"], s3_key)
            results.append(
                StadiumResponse(stadium=item, signedPhotoUrl=signed_url)
            )
        except Exception as e:
            Logger().exception(f"Failed to generate signed URL for stadium {item.stadiumName}: {e}")
            continue


def get_stadiums(ids="", name="", size=50):
    results = []
    table = StadiumsTable(dynamodb_res)

    if ids:
        try:
            clean_ids = list(
                set(int(clean_id) for id in ids.split(",") if (clean_id := id.strip()))
            )
        except ValueError as e:
            Logger().error(f"Invalid ID format: {e}")
            raise BadRequestException("Invalid ID format provided.")

        items = table.get_items([{"id": id} for id in clean_ids])
        generate_stadiums_response(items, results)
    elif name:
        formatted_name = format_query_name(name)
        words = formatted_name.split(" ")
        scan_filter = Attr("stadiumName").contains(words[0])
        for word in words[1:]:
            scan_filter &= Attr("stadiumName").contains(word)

        expression_attribute_names = {
            '#cap': 'capacity'
        }

        items = table.scan(filter=scan_filter, names=expression_attribute_names, size=size)
        generate_stadiums_response(items, results)
    else:
        Logger().error("ID or name must be specified")
        raise BadRequestException("ID or name must be specified")

    all_items = len(results) <= size
    results = results[:size]

    return StadiumsResponse(
        count=len(results),
        allItems=all_items,
        items=results,
        sizeLimit=size
    )


@http_request
def get_stadiums_handler(event: HttpRequestData, context):
    ids = event.queryParams.get("id", "")
    name = event.queryParams.get("", "").strip()
    size = int(event.queryParams.get("size", "200"))

    return get_stadiums(ids, name, size)
