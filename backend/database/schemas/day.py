from pydantic import BaseModel
from datetime import date

from database.schemas.recipes import Recipe
class DayBase(BaseModel):
    """Required inforamtion to create a day"""
    date : date

class CreateDay(DayBase):
    name : str
    menu_id : int
class Day(CreateDay):
    """"Full day modell"""
    id : int
    meal_plan : dict[str, list[Recipe]]
    class Config:
        orm_mode = True

class DB_Day(CreateDay):
    id : int
    meal_plan : dict[str, list[int]]
    class Config:
        orm_mode = True