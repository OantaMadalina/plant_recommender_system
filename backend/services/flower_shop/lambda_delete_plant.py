from __future__ import annotations
from dataclasses import dataclass
import boto3
import os
from services.flower_shop.utils import generate_signed_url
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException, NotFoundException
)
from bootcamp_lib.logger import Logger
from services.flower_shop.table_plant_data import (
    PlantDataTable, PlantDataModel
)

dynamodb_res = boto3.resource("dynamodb")
s3_client = boto3.client("s3")

@dataclass
class PlantResponse:
    plant: PlantDataModel
    signedPhotoUrl: str
        
def delete_plant(idPlant: str):
    
    table = PlantDataTable(dynamodb_res)
    plant = table.delete_item({"idPlant": idPlant}, return_values="ALL_OLD")
    
    if not plant.get("Attributes"):
        raise NotFoundException(f"Plant not found for ID {idPlant}")
    
# Delete the image from S3
    image_url = plant["Attributes"]["namePlant"]
    s3_key = f"FlowerShop/PlantImages/{image_url.replace(' ', '')}.png"
    try:
        s3_client.delete_object(Bucket=os.environ["BOOTCAMP_BUCKET"], Key=s3_key)
        Logger().info(f"Deleted image from S3: {s3_key}")
    except Exception as e:
        Logger().error(f"Error deleting image from S3: {e}")
        raise

@http_request()
def delete_plant_handler(event: HttpRequestData, context):
    try:
        idPlant = str(event.pathParams.get("id", "").strip())
    except Exception as e:
        Logger().error("Error found trying to get the plant ID: " + str(e))
        raise BadRequestException("Error found trying to get the plant ID: " + str(e))

    if not idPlant:
        raise BadRequestException(f"Invalid Plant ID {idPlant}")

    return delete_plant(idPlant)
