import boto3
from typing import List
from backend.bootcamp_lib.logger import Logger
from bootcamp_lib.lambda_middleware import (
    HttpRequestData, http_request
)
from services.recipe_share.table_food_recipes import (
    FoodRecipesTable, FoodRecipeModel
)

dynamodb = boto3.resource("dynamodb")


def get_recipes() -> List[FoodRecipeModel]:
    try:
        recipes = FoodRecipesTable(dynamodb).scan(size=100)
        return recipes
    except Exception as e:
        Logger().warning(f"Error fetching recipes: {e}")
        raise


@http_request()
def get_recipes_handler(request: HttpRequestData, _):
    return get_recipes()
