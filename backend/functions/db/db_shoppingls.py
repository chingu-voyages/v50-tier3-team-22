from sqlalchemy.orm import Session

from database.models.shoppingls import ShoppingList as ShoppingListModell 
from database.schemas.shoppingls import ShoppingListBase

def create_shopping_list(db : Session, shopping_list : ShoppingListBase) -> ShoppingListModell:
    db_shopping_list = ShoppingListModell(**shopping_list.dict())
    db.add(db_shopping_list)
    db.commit()
    db.refresh(db_shopping_list)

    return db_shopping_list

def delete_shopping_list(db : Session, id : int):
    db.query(ShoppingListModell).filter(ShoppingListModell.id == id).delete()
    db.commit()

def delete_shopping_lists(db : Session, owner_id : int):
    db.query(ShoppingListModell).filter(ShoppingListModell.owner_id == owner_id).delete()
    db.commit()

def get_shopping_lists_by_user(db : Session, owner_id : int) -> list[ShoppingListModell]:
    return db.query(ShoppingListModell).filter(ShoppingListModell.owner_id == owner_id).all()

def get_shopping_list_by_id(db:Session, id:int) -> ShoppingListModell | None:
    return db.query(ShoppingListModell).filter(ShoppingListModell.id == id).first()

def update_shopping_list(db : Session, id = int,  data_to_update = dict):
    db.query(ShoppingListModell).filter(ShoppingListModell.id == id).update(data_to_update)
    db.commit() 

def get_shoppig_list_of_menu(db : Session, menu_id : int) -> list[ShoppingListModell]:
    return db.query(ShoppingListModell).filter(ShoppingListModell.menu_id == menu_id).order_by(ShoppingListModell.created).all()