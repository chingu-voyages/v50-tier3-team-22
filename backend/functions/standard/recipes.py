from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import re

from database.schemas.recipes import Recipe, RecipeBase, RecipeCreate
from database.schemas.authentication import User

from functions.db.db_recipe import create_recipe, get_recipe_by_id

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

    recipe_out = recipe.__dict__
    recipe_out.pop('_sa_instance_state')
    recipe_out = Recipe(**recipe_out)

    return recipe_out
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
    recipe_out = recipe.__dict__
    recipe_out.pop('_sa_instance_state')
    recipe_out = Recipe(**recipe_out)

    return recipe_out
    #Return if possible