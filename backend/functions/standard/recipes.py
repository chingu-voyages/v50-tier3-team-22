from fastapi import HTTPException, status, UploadFile, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import re

from io import BytesIO

from functions.standard.image_manager import image_upload, get_image_url, delete_image, get_image

from database.schemas.recipes import Recipe, RecipeBase, RecipeCreate, UpdateRecipeData
from database.schemas.authentication import User

from functions.db.db_recipe import create_recipe, get_recipe_by_id, update_recipe, delete_recipe, get_favourite_recipes_by_user, get_recipes_by_user
from functions.db.db_ingredients import delete_ingredient

VALIDATION_ERROR = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "The data sent is invalid"
    )

RECIPE_OPTIONS = {
    "category" : {
        1 : "Breakfast",
        2 : "Lunch",
        3 : "Dinner",
        4 : "Snacks",
        5 : "Dessert"
    },
    "level": {
        1 : "Easy",
        2 : "Medium",
        3 : "Hard"
    }
}
#Constants for the recipe options

def add_recipe(data : RecipeBase, image : UploadFile | None, user : User, db_session : Session):
    if len(data.name) == 0:
        raise VALIDATION_ERROR
    if len(re.findall(pattern="[^a-zA-z0-9 ]", string=data.name)):
       raise VALIDATION_ERROR
    if data.cuisine != None:
        if len(data.cuisine) > 15 or len(re.findall(pattern="[^a-zA-Z]", string=data.cuisine)):
            raise VALIDATION_ERROR
    if data.time > 7200:
        raise VALIDATION_ERROR
    if data.level not in RECIPE_OPTIONS["level"].keys():
        raise VALIDATION_ERROR
    if data.category not in RECIPE_OPTIONS["category"].keys():
        raise VALIDATION_ERROR
    image_name = None
    image_url = None
    if image != None:
        image_name, image_url = image_upload(image=image)
    #image upload

    #input validation

    
    recipe = RecipeCreate(owner_id=user.id, image_name=image_name,**data.dict())
    #create object to add to db

    recipe = create_recipe(db=db_session, recipe=recipe)
    #add to db

    return Recipe(image_url=image_url, **recipe.dict())
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

    image_url = None
    if recipe.image_name != None:
        image_url = get_image_url(recipe.image_name)
    
    #Check if id is accessible by user

    return Recipe(image_url=image_url, **recipe.dict())
    #Return if possible

def update_recipe_content(id:int, image : UploadFile,  data : UpdateRecipeData, db_session : Session, user : User):
    data_to_update : dict = data.dict()

    print(data_to_update)
    for key, value in data.dict().items():
        if value == None:
            data_to_update.pop(key)
    #Clear update data

    if data.name != None:
        if len(data.name) == 0:
            raise VALIDATION_ERROR
        if len(re.findall(pattern="[^a-zA-z0-9 ]", string=data.name)):
            raise VALIDATION_ERROR
    
    if data.cuisine != None:
        if len(data.cuisine) > 15 or len(re.findall(pattern="[^a-zA-Z]", string=data.cuisine)):
            raise VALIDATION_ERROR
        
    if data.time != None:
        if data.time > 7200:
            raise VALIDATION_ERROR
        
    if data.level != None:
        if data.level not in RECIPE_OPTIONS["level"].keys():
            raise VALIDATION_ERROR
    
    if data.category != None:
        if data.category not in RECIPE_OPTIONS["category"].keys():
            raise VALIDATION_ERROR
    #Validate data
    recipe = get_recipe_by_id(db=db_session, id = id)
    
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
    image_url = None
    if image != None:
        _, image_url = image_upload(image=image, image_name=recipe.image_name)
    if recipe.image_name != None:
        image_url = get_image_url(recipe.image_name)

    if len(data_to_update) > 0:
        update_recipe(db=db_session, id=id, data_to_update=data_to_update)

    recipe = get_recipe_by_id(id=recipe.id, db=db_session)

    #Update data and retrieve info

    return Recipe(image_url=image_url,**recipe.dict())
    #return the updated data


def remove_recipe(id : int, db_session : Session, user : User):
    recipe = get_recipe_by_id(db=db_session, id=id)

    ingredient_ids = [ingredient["id"] for ingredient in recipe.ingredients]
    #saving the ingredient ids so will be able to delete

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
    if recipe.image_name != None:
        delete_image(recipe.image_name)
    #Deleting the image

    delete_recipe(id=id, db=db_session)
    #delete recipe

    recipes = get_recipes_by_user(db=db_session, owner_id=user.id)

    present_ingredient_ids = []

    for recipe in recipes:
        if len(recipe.ingredients) > 1:
            present_ingredient_ids.append(*[ingredient["id"] for ingredient in recipe.ingredients])
        elif len(recipe.ingredients) == 1:
            present_ingredient_ids.append(recipe.ingredients[0]["id"])

    #Creating a list with all the ingredient ids present in recipes
    for ingredient_id in ingredient_ids:
        if ingredient_id not in present_ingredient_ids:
            delete_ingredient(db=db_session, id=ingredient_id)
    
    #Removing the ingredient if this was the only recipe it was present in
    return

def get_recipes(is_favourite : bool, db_session : Session, user : User):
    if is_favourite:
        return get_favourite_recipes_by_user(db=db_session, owner_id=user.id)
    return get_recipes_by_user(db=db_session, owner_id=user.id)

def retrieve_image(recipe_id : int, db_session : Session, user : User):
    recipe = get_recipe_by_id(db=db_session, id=recipe_id)

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
    if recipe.image_name == None:
        return {"No image for this recipe"}

    image = get_image(image_name=recipe.image_name)

    #getting the image 
    image_stream = BytesIO(image)
    #returning the image url
    return StreamingResponse(content=image_stream, media_type="image/jpeg")