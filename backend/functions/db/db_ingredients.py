from sqlalchemy.orm import Session

from database.models.ingredient import Ingredient as IngredientModell
from database.schemas.ingredients import AddIngredient

def create_ingredient(db : Session, ingredient : AddIngredient) -> IngredientModell:
    db_ingredient = IngredientModell(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient

def delete_ingredient(db : Session, id : int):
    db.query(IngredientModell).filter(IngredientModell.id == id).delete()

def delete_ingredients(db : Session, owner_id : int):
    db.query(IngredientModell).filter(IngredientModell.owner_id == owner_id).delete()

def get_ingredient(db : Session, name : str, owner_id : int) -> IngredientModell | None:
    return db.query(IngredientModell).filter(IngredientModell.owner_id == owner_id).filter(IngredientModell.name == name).first()

def get_ingredients_by_user(db : Session, owner_id : int) -> list[IngredientModell]:
    return db.query(IngredientModell).filter(IngredientModell.owner_id == owner_id).all()

def get_ingredient_by_name(db:Session, name:str) -> IngredientModell | None:
    return db.query(IngredientModell).filter(IngredientModell.name == name).first()