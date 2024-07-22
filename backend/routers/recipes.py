from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from database.database_services import get_db

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

from database.schemas.recipes import  Recipe, CreateRecipeForm, UpdateRecipeForm
from functions.standard.recipes import add_recipe, find_recipe, update_recipe_content, remove_recipe, get_recipes, retrieve_image, RECIPE_OPTIONS

router = APIRouter()

@router.get("/recipe/options", response_model=dict, tags=["Recipe"], status_code=status.HTTP_200_OK)
async def send_options():
    return RECIPE_OPTIONS

@router.get("/recipes", tags=["Recipe"], status_code=status.HTTP_200_OK)
async def get_recipes_of_user(filter_fav : bool = False, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return get_recipes(is_favourite=filter_fav, db_session=db, user=user)

@router.get("/recipe/{recipe_id}", response_model=Recipe, tags=["Recipe"], status_code=status.HTTP_200_OK)
async def get_recipe(recipe_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return find_recipe(id=recipe_id, user=user, db_session=db)

@router.post("/recipe", tags=["Recipe"], status_code=status.HTTP_201_CREATED)
async def create_new_recipe(
    recipe : CreateRecipeForm = Depends(), image : UploadFile | None = File(default=None), 
    db : Session = Depends(get_db), user : User = Depends(authenticate)
    ):
    return add_recipe(data=recipe.get_recipe_base(),image=image, user=user, db_session=db)

@router.put("/recipe/{recipe_id}", response_model=Recipe, tags=["Recipe"], status_code=status.HTTP_202_ACCEPTED)
async def update_recipe(
    recipe_id : int, recipe : UpdateRecipeForm = Depends(), image : UploadFile | None = File(default=None), 
    db : Session = Depends(get_db), user : User = Depends(authenticate)
    ):
    return update_recipe_content(id = recipe_id, image=image ,data = recipe.get_recipe_base(), user = user, db_session=db)

@router.delete("/recipe/{recipe_id}", response_model=None, tags=["Recipe"], status_code=status.HTTP_200_OK)
async def delete_recipe(recipe_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return remove_recipe(id=recipe_id, db_session=db, user=user)

@router.get("/recipe/{recipe_id}/image", tags=["Recipe"], status_code=status.HTTP_200_OK)
async def get_recipe(recipe_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return retrieve_image(recipe_id=recipe_id, db_session=db, user=user)