from sqlalchemy.orm import Session

from database.models.recipe import Recipe as RecipeModel
from database.schemas.recipes import RecipeCreate

def create_recipe(db : Session, recipe : RecipeCreate) -> RecipeModel:
    db_recipe = RecipeModel(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe

def delete_recipe(db : Session, id : int):
    db.query(RecipeModel).filter(RecipeModel.id == id).delete()
    db.commit()

def delete_recipes(db : Session, owner_id : int):
    db.query(RecipeModel).filter(RecipeModel.owner_id == owner_id).delete()

def get_recipe_by_id(db : Session, id : int) -> RecipeModel | None:
    return db.query(RecipeModel).filter(RecipeModel.id == id).first()

def get_recipe_by_user(db : Session, owner_id : int) -> list[RecipeModel]:
    return db.query(RecipeModel).filter(RecipeModel.owner_id == owner_id).all()
