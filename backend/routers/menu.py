from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from datetime import date

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

from database.schemas.day import DayBase, Day
from database.schemas.recipes import RecipeId
from database.schemas.menu import FullMenu

from functions.standard.menu import MEAL_PLAN_OPTIONS, add_recipe_to_menu, delete_recipe_from_menu, get_weekly_menu

router = APIRouter()

@router.get("/menu/day/options", response_model=list, tags=["Menu"], status_code=status.HTTP_200_OK)
async def get_options():
    return MEAL_PLAN_OPTIONS

@router.get("/menu", response_model=FullMenu, tags=["Menu"], status_code=status.HTTP_200_OK)
async def return_menu_by_date(date : date, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return get_weekly_menu(date=date, db_session=db, user=user)

@router.post("/menu/day/{meal}", response_model= Day, tags=["Menu"], status_code=status.HTTP_201_CREATED)
async def add_recipe_to_day(meal : str, recipe_id : RecipeId, day : DayBase, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return add_recipe_to_menu(meal=meal, data=day, recipe_id=recipe_id, db_session=db, user=user)

@router.delete("/menu/day/{meal}", response_model=None, tags=["Menu"], status_code=status.HTTP_202_ACCEPTED)
async def delete_recipe(meal : str, recipe_id : RecipeId, day : DayBase, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return delete_recipe_from_menu(meal=meal, recipe_id=recipe_id, date=day.date, db_session=db, user=user)