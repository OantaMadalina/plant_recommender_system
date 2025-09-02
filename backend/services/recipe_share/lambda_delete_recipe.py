import boto3

from bootcamp_lib.lambda_middleware import (
    http_request, HttpRequestData, BadRequestException, NotFoundException
)
from bootcamp_lib.logger import Logger
from services.recipe_share.table_food_recipes import FoodRecipesTable

dynamodb = boto3.resource("dynamodb")
s3_client = boto3.client('s3')

recipes_table = FoodRecipesTable(dynamodb_resource=dynamodb)
bucket_name = 'bootcampBucket'


def delete_recipe(recipe_id: str):
    table = FoodRecipesTable(dynamodb)
    recipe = table.delete_item({"id": recipe_id}, return_values="ALL_OLD")

    if not recipe.get("Attributes"):
        raise NotFoundException(f"Recipe not found for ID {recipe_id}")

    image_url = recipe["Attributes"].get("imageUrl")

    if image_url:
        s3_key = image_url.split(f"{bucket_name}/")[-1]
        s3_client.delete_object(Bucket=bucket_name, Key=s3_key)


@http_request()
def delete_recipe_handler(request: HttpRequestData, _):
    try:
        recipe_id = request.pathParams.get("id")
    except Exception as e:
        Logger().error("Error trying to delete recipe: " + str(e))
        raise BadRequestException("Unable to delete recipe")

    return delete_recipe(recipe_id)
