from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import re
import json

from database.schemas.authentication import User
from database.schemas.recipes import Recipe
from database.schemas.ingredients import FullIngredient, CreateIngredient, AddIngredient

from functions.db.db_ingredients import get_ingredients_by_user, get_ingredient_by_name, create_ingredient, delete_ingredient
from functions.db.db_recipe import get_recipe_by_id, update_recipe, get_recipes_by_user

VALIDATION_ERROR = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "The data sent is invalid"
    )

INGREDIENT_OPTIONS = {
    1 : {
        "name" : "Liquid",
        "options" : {
            1: "ml",
            2: "dl",
            3: "l",
            4: "table spoon",
            5: "tea spoon",
            6: "cup"
        }
    },
    2 : {
        "name" : "Solid",
        "options" : {
            1: "g",
            2: "kg",
            3: "table spoon",
            4: "tea spoon",
            5: "cup"
        }
    },
    3 : {
        "name" : "Piece",
        "options" : {
            1 : "piece",
            2 : "head",
        }
    }
}

def get_users_ingredients(db_session : Session, user : User):
    ingredients = get_ingredients_by_user(db=db_session, owner_id=user.id)
    return ingredients

def create_ingredient_to_recipe(recipe_id : int, data : CreateIngredient, db_session : Session, user : User):
    recipe = get_recipe_by_id(db=db_session, id=recipe_id)
    if recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe with this id was not found"
        )
    
    if recipe.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="You cannot access this recipe with this id"
        )
    
    if len(re.findall(pattern="[^a-zA-Z ]", string=data.name)):
        raise VALIDATION_ERROR
    
    if data.type not in INGREDIENT_OPTIONS.keys():
        raise VALIDATION_ERROR
    
    if data.unit not in INGREDIENT_OPTIONS[data.type]["options"].keys():
        raise VALIDATION_ERROR
    
    #data validation
    data.name = data.name.casefold()

    ingredients : list = recipe.ingredients

    for ingredient in ingredients:
        if ingredient["name"] == data.name:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Ingredient with this name is already present"
            )

    

    #adding ingredient to list 
    db_ingredient = get_ingredient_by_name(db=db_session, name=data.name)

    if db_ingredient == None:
        db_ingredient = create_ingredient(
            db=db_session, 
            ingredient=AddIngredient(owner_id=user.id, **data.dict())
            )

    #add ingredient if not already in db

    ingredients.append(FullIngredient(id = db_ingredient.id, **data.dict()).dict())

    update_recipe(db=db_session, id=recipe.id, data_to_update={
        "ingredients" : ingredients
    })

    #save ingerdients to recipe
    
    db_recipe = get_recipe_by_id(db=db_session, id=recipe.id)

    return db_recipe
    #create the recipe to return

def delete_ingredient_of_recipe(recipe_id : int, ingredient_id : int, db_session : Session, user : User):
    recipe = get_recipe_by_id(db=db_session, id=recipe_id)

    if recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe with this id was not found"
        )
    
    if recipe.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="You cannot access this recipe with this id"
        )
    #returning recipe if it exists and accessible

    new_ingredients = [ingredient for ingredient in recipe.ingredients if ingredient["id"] != ingredient_id]

    #Creating the new ingredient list without the ingredietn

    if len(new_ingredients) == len(recipe.ingredients):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ingredient with this id was not found in ingredietns"
        )
    #Checking if the ingredient was removed

    update_recipe(db=db_session, id=recipe.id, data_to_update={"ingredients" : new_ingredients})

    #Updating the ingredient
    
    recipes = get_recipes_by_user(db=db_session, owner_id=user.id)
    
    ingredient_ids = []

    for recipe in recipes:
        if len(recipe.ingredients) > 1:
            ingredient_ids.append(*[ingredient["id"] for ingredient in recipe.ingredients])
        elif len(recipe.ingredients) == 1:
             ingredient_ids.append(recipe.ingredients[0]["id"])

    #Creating a list with all the ingredient ids present in recipes

    if ingredient_id not in ingredient_ids:
        delete_ingredient(db=db_session, id=ingredient_id)
    
    #Removing the ingredient if this was the only recipe it was present in

    return