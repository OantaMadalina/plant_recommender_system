import boto3
from backend.services.recipe_share.table_food_recipes import FoodRecipesTable, FoodRecipeModel
from bootcamp_lib.logger import Logger
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, InternalServerErrorException, http_request
)
import uuid
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


@http_request(
    request_type="POST",
    validation={
        "recipeName": {"required": True},
        "author": {"required": True},
        "ingredients": {"required": True},
        "category": {"required": True}
    }
)
def create_recipe_handler(request: HttpRequestData, _):
    try:
        data = request.get('body', {})
        Logger().info(f"Received data: {data}")

        recipe_id = str(uuid.uuid4())
        image_data = data['imageData']

        if image_data:
            image_name = f"{recipe_id}.jpg"
            image_url = upload_image_to_s3(image_data, image_name)
        else:
            image_url = None

        recipe = FoodRecipeModel(
            id=recipe_id,
            recipeName=data['recipeName'],
            author=data['author'],
            description=data.get('description', ''),
            ingredients=data['ingredients'],
            category=data['category'],
            calories=data.get('calories', 0),
            protein=data.get('protein', 0.0),
            carbohydrates=data.get('carbohydrates', 0.0),
            fats=data.get('fats', 0.0),
            imageUrl=image_url,
        )

        recipes_table.put_item(recipe)
        Logger().info(f"Recipe created successfully: {recipe.to_dict()}")

        return recipe

    except Exception as e:
        Logger().exception("Error during recipe creation: " + e)
        raise InternalServerErrorException
