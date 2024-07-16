from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import re

from database.schemas.recipes import Recipe, RecipeBase, RecipeCreate, UpdateRecipeData
from database.schemas.authentication import User

from functions.db.db_recipe import create_recipe, get_recipe_by_id, update_recipe, delete_recipe

VALIDATION_ERROR = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "The data sent is invalid"
    )

def add_recipe(data : RecipeBase, user : User, db_session : Session):
    if len(data.name) == 0:
        raise VALIDATION_ERROR
    if len(re.findall(pattern="[^a-zA-z0-9 ]", string=data.name)):
       raise VALIDATION_ERROR
    #input validation
    
    recipe = RecipeCreate(owner_id=user.id, **data.dict())
    #create object to add to db

    recipe = create_recipe(db=db_session, recipe=recipe)
    #add to db

    return Recipe(**recipe.dict())
    #return db modell

def find_recipe(id : int, user : User,  db_session : Session):
    recipe = get_recipe_by_id(id=id, db=db_session)
    
    if  recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe with this id was not found"
        )
    if recipe.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to access this recipe"
        )
    
    #Check if id is accessible by user

    return Recipe(**recipe.dict())
    #Return if possible

def update_recipe_content(id:int, data : UpdateRecipeData, db_session : Session, user : User):
    data_to_update : dict = data.dict()

    for key, value in data.dict().items():
        if value == None:
            data_to_update.pop(key)
    #Clear update data

    if data.name != None:
        if len(data.name) == 0:
            raise VALIDATION_ERROR
        if len(re.findall(pattern="[^a-zA-z0-9 ]", string=data.name)):
            raise VALIDATION_ERROR
    #Validate data
    recipe = get_recipe_by_id(db=db_session, id = data.id)
    
    if  recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe with this id was not found"
        )
    if recipe.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to change and access this recipe"
        )

    #Check ownership
    update_recipe(db=db_session, id=id, data_to_update=data_to_update)

    recipe = get_recipe_by_id(id=recipe.id, db=db_session)

    #Update data and retrieve info

    return Recipe(**recipe.dict())
    #return the updated data


def remove_recipe(id : int, db_session : Session, user : User):
    recipe = get_recipe_by_id(db=db_session, id=id)

    if recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe with this id was not found"
        )
    elif recipe.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unautrhorized to delete or access this recipe"
        )
    
    #Getting the recipe from db and handling unathorized access and not found

    delete_recipe(id=id, db=db_session)

    #Deleting the recipe
    return