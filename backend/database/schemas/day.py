from pydantic import BaseModel
from datetime import datetime

from database.schemas.recipes import Recipe

class CreateDay(BaseModel):
    """Required inforamtion to create a day"""
    date : datetime
    
class Day(CreateDay):
    """"Full day modell"""
    id : int
    name : str
    meal_plan : dict[str, list[Recipe]]
    menu_id : int