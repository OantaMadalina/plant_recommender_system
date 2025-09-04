from __future__ import annotations
from dataclasses import dataclass
import boto3
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from services.flower_shop.utils import generate_signed_url
from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException, NotFoundException
)
from bootcamp_lib.logger import Logger
from services.flower_shop.table_plant_data import (
    PlantDataTable, PlantDataModel
)

# Initialize DynamoDB resource
dynamodb_res = boto3.resource("dynamodb")
plant_table = PlantDataTable(dynamodb_res)

# Logger setup
logger = Logger()

def lambda_handler(event, context):
    try:
        # Parse input plant ID from the event
        plant_id = event.get('plant_id')
        if not plant_id:
            raise BadRequestException("Input plant ID is required.")

        # Fetch data from DynamoDB
        plant_data = fetch_plant_data()
        
        # Preprocess data for K-Means
        data_matrix, plant_ids = preprocess_data(plant_data)
        
        # Apply K-Means clustering
        kmeans_result = apply_kmeans(data_matrix)
        
        # Find the cluster for the input plant ID
        recommended_plants = recommend_plants(plant_id, kmeans_result, plant_data, plant_ids)
        
        # Return the result
        return {
            'statusCode': 200,
            'body': json.dumps(recommended_plants)
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def fetch_plant_data():
    # Scan the DynamoDB table
    response = plant_table.scan()
    items = response['Items']
    return items

def preprocess_data(items):
    # Extract relevant features for clustering and keep track of plant IDs
    features = []
    plant_ids = []
    for item in items:
        features.append([
            float(item['Sunlight-Hours']),
            float(item['Water-Frequency']),
            float(item['Temperature']),
            float(item['Humidity'])
        ])
        plant_ids.append(item['Plant-ID'])
    return np.array(features), plant_ids

def apply_kmeans(data_matrix, n_clusters=3):
    # Apply K-Means algorithm
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(data_matrix)
    
    # Calculate silhouette score
    silhouette_avg = silhouette_score(data_matrix, kmeans.labels_)
    
    return {
        'centroids': kmeans.cluster_centers_,
        'labels': kmeans.labels_,
        'silhouette_score': silhouette_avg
    }

def recommend_plants(plant_id, kmeans_result, plant_data, plant_ids):
    # Find the index of the input plant ID
    try:
        plant_index = plant_ids.index(plant_id)
    except ValueError:
        raise NotFoundException(f"Plant ID {plant_id} not found.")
    
    # Get the cluster label for the input plant
    input_label = kmeans_result['labels'][plant_index]
    
    # Find plants in the same cluster
    recommended_plants = []
    for idx, label in enumerate(kmeans_result['labels']):
        if label == input_label and plant_ids[idx] != plant_id:
            recommended_plants.append(plant_data[idx])
    
    return recommended_plants
