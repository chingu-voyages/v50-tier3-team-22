from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

from database.schemas.day import DayBase, Day
from database.schemas.recipes import RecipeId

from functions.standard.menu import MEAL_PLAN_OPTIONS, add_recipe_to_menu

router = APIRouter()

@router.get("/menu/day/options", response_model=list, tags=["Menu"], status_code=status.HTTP_200_OK)
async def get_options():
    return MEAL_PLAN_OPTIONS

@router.post("/menu/day/{meal}", response_model= Day, tags=["Menu"], status_code=status.HTTP_201_CREATED)
async def add_recipe_to_day(meal : str, recipe_id : RecipeId, day : DayBase, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return add_recipe_to_menu(meal=meal, data=day, recipe_id=recipe_id, db_session=db, user=user)