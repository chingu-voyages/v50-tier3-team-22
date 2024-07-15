from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

from database.schemas.recipes import RecipeBase, Recipe
from functions.standard.recipes import add_recipe, find_recipe

router = APIRouter()

@router.get("/recipe/{recipe_id}",response_model=Recipe, tags=["Recipe"], status_code=status.HTTP_200_OK)
async def get_recipe(recipe_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return find_recipe(id=recipe_id, user=user, db_session=db)

@router.post("/recipe", response_model=Recipe , tags=["Recipe"], status_code=status.HTTP_201_CREATED)
async def create_new_recipe(recipe : RecipeBase, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return add_recipe(data=recipe, user=user, db_session=db)

