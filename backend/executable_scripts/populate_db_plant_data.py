import json
import os
import boto3
from dataclasses import dataclass
from typing import List
from bootcamp_lib.logger import Logger
import sys
sys.path.append('/path/to/bootcamp_lib')

# Initialize DynamoDB resource
dynamodb_res = boto3.resource("dynamodb", verify=False)

# Define the PlantDataModel using dataclass
@dataclass
class PlantDataModel:
    plantID: int
    plantRating: int
    plantName: str
    soilType: str
    sunlightHours: int
    waterFrequency: str
    fertilizerType: str
    temperature: float
    humidity: float
    location: str
    age: int

# Define the PlantDataTable class
class PlantDataTable:
    def __init__(self, dynamodb_resource):
        self.table = dynamodb_resource.Table('PlantDataTable')

    def put_items(self, items: List[PlantDataModel]):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item.__dict__)

# Function to load plant data from a JSON file
def load_plant_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Main function to populate the DynamoDB table
def main():
    logger = Logger()
    plant_data_table = PlantDataTable(dynamodb_res)

    # Path to the JSON file containing plant data
    file_path = "D:/plant_recommender_system/backend/scripts/plant_data.json"

    # Load plant data from the JSON file
    try:
        plant_data_list = load_plant_data(file_path)
    except Exception as e:
        logger.exception(f"Error loading plant data: {str(e)}")
        return

    # Convert JSON data to PlantDataModel instances
    plants = []
    for plant_data in plant_data_list:
        try:
            plant = PlantDataModel(
                plantID=plant_data["Plant-ID"],
                plantRating=plant_data["Plant-Rating"],
                plantName=plant_data["Plant-Name"],
                soilType=plant_data["Soil-Type"],
                sunlightHours=plant_data["Sunlight-Hours"],
                waterFrequency=plant_data["Water-Frequency"],
                fertilizerType=plant_data["Fertilizer-Type"],
                temperature=plant_data["Temperature"],
                humidity=plant_data["Humidity"],
                location=plant_data["Location"],
                age=plant_data["Age"]
            )
            plants.append(plant)
        except KeyError as e:
            logger.error(f"Missing key in plant data: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing plant data: {str(e)}")

    # Add plant instances to the DynamoDB table
    try:
        plant_data_table.put_items(plants)
        logger.info("Successfully added plant data to the DynamoDB table.")
    except Exception as e:
        logger.exception(f"Error adding plant data to the DynamoDB table: {str(e)}")

if __name__ == "__main__":
    main()
