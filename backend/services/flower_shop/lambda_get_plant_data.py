from logging import Logger
from dataclasses import dataclass
from typing import List
import os
import boto3
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, lambda_logger
)
from services.flower_shop.utils import generate_signed_url
from services.flower_shop.table_plant_data import (
    PlantDataTable, PlantDataModel
)

dynamodb_res = boto3.resource("dynamodb")

plant_table = PlantDataTable(dynamodb_res)

@dataclass
class PlantResponse:
    plant: PlantDataModel
    signedPhotoUrl: str

@dataclass
class PlantsResponse:
    items: list[PlantResponse]

def generate_response_with_photos(items: List[PlantDataModel]):
    results = []

    for item in items:
        s3_key = (
            "FlowerShop/PlantImages/"
            f"{item.namePlant.replace(' ', '')}.png"
        )
        signed_url = generate_signed_url(os.environ["BOOTCAMP_BUCKET"], s3_key)
        results.append(
            PlantResponse(plant=item, signedPhotoUrl=signed_url)
        )
    
    return results

def get_plants() -> List[PlantDataModel]:
    try:
        plants = PlantDataTable(dynamodb_res).scan(size=100)
        return generate_response_with_photos(plants)
    except Exception as e:
        Logger().warning(f"Error fetching plants: {e}")
        raise

@http_request()
@lambda_logger(log_input=True)
def get_plant_data_handler(request: HttpRequestData, _):
    return get_plants()
