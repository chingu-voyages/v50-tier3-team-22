from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

from functions.standard.ingredients import get_users_ingredients, INGREDIENT_OPTIONS, create_ingredient_to_recipe, delete_ingredient_of_recipe
from database.schemas.ingredients import Ingredient, CreateIngredientForm, CreateIngredient
from database.schemas.recipes import Recipe

router = APIRouter()

@router.get("/ingredient/options", response_model=dict[str, dict], tags=["Ingredient"], status_code=status.HTTP_200_OK)
async def return_ingredient_options():
    return INGREDIENT_OPTIONS

@router.get("/ingredients", response_model=list[Ingredient], tags=["Ingredient"], status_code=status.HTTP_200_OK)
async def get_my_ingredients(db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return get_users_ingredients(db_session=db, user=user)

@router.post("/{recipe_id}/ingredient", response_model=Recipe, tags=["Ingredient"], status_code=status.HTTP_201_CREATED)
async def add_ingredient_to_recipe(recipe_id : int, ingredient: CreateIngredientForm = Depends(), db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return create_ingredient_to_recipe(recipe_id=recipe_id, data=CreateIngredient(**ingredient.__dict__), db_session=db, user=user)

@router.delete("/{recipe_id}/ingredient", tags=["Ingredient"], status_code=status.HTTP_202_ACCEPTED)
async def delete_ingredient_from_recipe(recipe_id : int, ingredient_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return delete_ingredient_of_recipe(recipe_id=recipe_id, ingredient_id=ingredient_id, db_session=db, user=user)