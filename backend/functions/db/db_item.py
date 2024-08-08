from sqlalchemy.orm import Session

from database.models.item import Item as ItemModell 
from database.schemas.item import ItemBase

def create_item(db : Session, item : ItemBase) -> ItemModell:
    db_item = ItemModell(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def get_item_by_id(db:Session, id :int) -> ItemModell | None:
    return db.query(ItemModell).filter(ItemModell.id == id).first()

def delete_item(db : Session, id : int):
    db.query(ItemModell).filter(ItemModell.id == id).delete()
    db.commit()

def delete_items(db : Session, shopping_list_id : int):
    db.query(ItemModell).filter(ItemModell.shopping_list_id == shopping_list_id).delete()
    db.commit()

def update_item(db : Session, id = int,  data_to_update = dict):
    db.query(ItemModell).filter(ItemModell.id == id).update(data_to_update)
    db.commit()