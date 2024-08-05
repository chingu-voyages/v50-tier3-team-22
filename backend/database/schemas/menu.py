from pydantic import BaseModel
from datetime import date

from database.schemas.day import DB_Day

class CreateMenu(BaseModel):
    """The base modell for menus the info that the user provides"""
    start_date : date
    end_date : date
    owner_id : int

class Menu(CreateMenu):
    """"Full menu modell with all information as stored in datatbase"""
    id : int
    days : list
    class Config:
        orm_mode = True

class FullMenu(CreateMenu):
    """"Full menu modell with all information to return to the user"""
    id : int
    days : list[DB_Day]