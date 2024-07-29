from sqlalchemy.orm import Session

from database.models.menu import Menu as MenuModell

from database.schemas.menu import CreateMenu

def create_menu(db : Session, menu : CreateMenu) -> MenuModell:
    db_menu = MenuModell(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    return db_menu

def update_menu(db : Session,id = int,  data_to_update = dict):
    db.query(MenuModell).filter(MenuModell.id == id).update(data_to_update)
    db.commit()
    
def delete_menu(db : Session, id : int):
    db.query(MenuModell).filter(MenuModell.id == id).delete()
    db.commit()

def delete_menus(db : Session, owner_id : int):
    db.query(MenuModell).filter(MenuModell.owner_id == owner_id).delete()

def get_menu_by_id(db : Session, id : int) -> MenuModell | None:
    return db.query(MenuModell).filter(MenuModell.id == id).first()