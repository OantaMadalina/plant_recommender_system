import boto3
from backend.services.recipe_share.table_food_recipes import FoodRecipesTable, FoodRecipeModel
from bootcamp_lib.logger import Logger
from bootcamp_lib.lambda_middleware import (
    BadRequestException,
    HttpRequestData,
    InternalServerErrorException,
    NotFoundException,
    http_request
)
import base64

dynamodb = boto3.resource('dynamodb', verify=False)
s3_client = boto3.client('s3')

recipes_table = FoodRecipesTable(dynamodb_resource=dynamodb)
bucket_name = 'bootcampBucket'


def upload_image_to_s3(image_data: str, image_name: str) -> str:
    image_bytes = base64.b64decode(image_data)
    directory = "FoodRecipes"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{directory}/{image_name}",
        Body=image_bytes, ContentType='image/jpeg'
        )
    return f"s3://{bucket_name}/{directory}/{image_name}"


def update_recipe(id: str, request: HttpRequestData) -> FoodRecipeModel:
    existing_recipe = recipes_table.get_item({"id": id})

    if not existing_recipe:
        raise NotFoundException("Recipe not found")

    updated_recipe = FoodRecipeModel(**existing_recipe.to_dict())

    updated_fields = request.dictBody.copy()

    for field in updated_fields:
        updated_recipe[field] = updated_fields.get(field)

    data = request.get('body', {})
    image_data = data['imageData']

    if image_data:
        image_name = f"{existing_recipe.id}.jpg"
        updated_recipe["imageUrl"] = upload_image_to_s3(image_data, image_name)

    try:
        recipes_table.put_item(FoodRecipeModel(updated_recipe))
    except Exception:
        Logger().exception(f"Error updating recipe {id}")
        raise InternalServerErrorException(f"Unable to update recipe {id}")

    return updated_recipe


@http_request(
    request_type="PUT"
)
def update_recipe_handler(request: HttpRequestData, _):
    try:
        recipe_id = request.pathParams.get("id")
    except Exception as e:
        Logger().error("Error trying to update recipe: " + str(e))
        raise BadRequestException("Unable to update recipe")

    return update_recipe(recipe_id, request)
