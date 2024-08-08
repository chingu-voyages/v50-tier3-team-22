from pydantic import BaseModel

class ItemBase(BaseModel):
    """The schema for creating the item"""
    name : str
    type : int
    unit : int
    amount : int
    shopping_list_id : int

class Item(ItemBase):
    """Shema for full item in database"""
    id : int
    is_checked : bool
    
    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    """Schema to update item"""
    id : int
    name : str | None  = None
    unit : int | None = None
    amount : int | None = None
    is_checked : bool | None = None