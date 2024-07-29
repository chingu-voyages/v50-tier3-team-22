from pydantic import BaseModel
from datetime import datetime

from database.schemas.ingredients import FullIngredient

class CreateMenu(BaseModel):
    """The base modell for menus the info that the user provides"""
    start_date : datetime
    end_date : datetime

class Menu(CreateMenu):
    """"Full menu modell with all information"""
    id : int
    ingredients : list[FullIngredient]
    days : list
    owner_id : int
