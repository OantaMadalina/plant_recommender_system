import boto3
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request, BadRequestException
)
from bootcamp_lib.logger import Logger
from services.recipe_share.table_food_recipes import (
    FoodRecipesTable, FoodRecipeModel
)

dynamodb = boto3.resource("dynamodb")


def get_recipe_by_id(recipe_id: str) -> FoodRecipeModel:
    try:
        recipe = FoodRecipesTable(dynamodb).get_item(key={"id": recipe_id})

        if not recipe:
            raise BadRequestException("Recipe not found.")

        return recipe
    except Exception as e:
        raise e


@http_request()
def get_recipe_by_id_handler(request: HttpRequestData, _):
    try:
        recipe_id = request.pathParams.get("id")

        if not recipe_id:
            raise BadRequestException("Invalid ID")

        recipe = get_recipe_by_id(recipe_id)
        return recipe
    except Exception as e:
        Logger().exception("Error getting recipe details: " + e)
        raise BadRequestException
