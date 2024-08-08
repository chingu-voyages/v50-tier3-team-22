from pydantic import BaseModel
from datetime import datetime

from database.schemas.item import Item

class ShoppingListBase(BaseModel):
    """The schema for creating the shopping list"""
    menu_id : int
    created : datetime
    owner_id : int

class ShoppingList(ShoppingListBase):
    """Shema for full shopping list"""
    id : int
    items : list[Item]
    
    class Config:
        orm_mode = True
    