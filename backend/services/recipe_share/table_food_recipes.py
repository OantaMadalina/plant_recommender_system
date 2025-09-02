from typing import ClassVar, List
from dataclasses import dataclass, field

from bootcamp_lib.dynamodb_model import DynamoDbModel
from bootcamp_lib.dynamodb import DynamodbTable, DynamodbCachedTable


@dataclass
class FoodRecipeModel(DynamoDbModel):
    id: str = ""
    recipeName: str = ""
    author: str = ""
    description: str = ""
    ingredients: List[str] = field(default_factory=list)
    category: str = ""
    calories: int = 0
    protein: float = 0.0
    carbohydrates: float = 0.0
    fats: float = 0.0
    imageUrl: str = ""

    _validations: ClassVar[dict] = {
        "id": {
            "required": True
        },
        "recipeName": {
            "required": True
        },
        "author": {
            "required": True
        },
        "description": {
            "required": False
        },
        "ingredients": {
            "required": True
        },
        "category": {
            "required": True
        },
        "calories": {
            "required": False
        },
        "protein": {
            "required": False
        },
        "carbohydrates": {
            "required": False
        },
        "fats": {
            "required": False
        },
        "imageUrl": {
            "required": False
        }
    }


class FoodRecipesTable(DynamodbTable[FoodRecipeModel]):
    table = "food-recipes"
    model_type = FoodRecipeModel


class FoodRecipesCache(DynamodbCachedTable[FoodRecipeModel]):

    def __init__(self, dynamodb_resource=None):
        super().__init__()
        self._table = FoodRecipesTable(dynamodb_resource)
        self._items = dict()

    def _get_items(self, keys: List[dict]):
        food_recipes = self._table.get_items(keys)
        for food_recipe in food_recipes:
            self._items[food_recipe.id] = food_recipe

    def _get_item(self, key: dict):
        if item := self._table.get_item(key):
            self._items[item.id] = item
