from pydantic import BaseModel
from fastapi import Form

class IngredientBase(BaseModel):
    """Schema to database of ingredient"""
    name : str
    type : int

class AddIngredient(IngredientBase):
    owner_id : int

class Ingredient(AddIngredient):
    """Full ingredient in database"""
    id : int
    
class FullIngredient(IngredientBase):
    """Ingredient to add to recipe"""
    amount : int
    unit : int


class CreateIngredientForm:
    def __init__(
        self,
        name : str = Form(),
        type : str = Form(),
        amount : int = Form(),
        unit : int = Form()
    ):
        self.name = name
        self.type = type
        self.amount = amount
        self.unit = unit

    def get_recipe_schema(self) -> FullIngredient:
        return FullIngredient(**self.__dict__)
