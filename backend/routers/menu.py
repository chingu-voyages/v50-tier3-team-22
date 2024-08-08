from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from datetime import date

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

from database.schemas.day import DayBase, Day
from database.schemas.recipes import RecipeId
from database.schemas.menu import FullMenu
from database.schemas.shoppingls import ShoppingList
from database.schemas.item import ItemUpdate

from functions.standard.menu import MEAL_PLAN_OPTIONS, add_recipe_to_menu, delete_recipe_from_menu, get_weekly_menu, generate_shopping_list, delete_shopping_list_from_db, delete_shoppinglist_item, update_item_data, get_shopping_list_from_db

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

@router.get("/menu/{menu_id}/shoppinglist", response_model=list[ShoppingList], tags=["Menu"], status_code=status.HTTP_200_OK)
async def shopping_list_for_menu(menu_id : int, generate_new : bool = False, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return generate_shopping_list(menu_id=menu_id, generate_new=generate_new, db_session=db, user=user)

@router.get("/menu/shoppinglists", response_model=list[ShoppingList], tags=["Menu"], status_code=status.HTTP_200_OK)
async def get_users_shopping_lists(user : User = Depends(authenticate)):
    return user.shopping_lists

@router.get("/menu/shoppinglist/{shopping_list_id}", response_model=ShoppingList, tags=["Menu"], status_code=status.HTTP_200_OK)
async def get_shopping_list(shopping_list_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return get_shopping_list_from_db(id=shopping_list_id, db_session=db, user=user)

@router.put("/menu/shoppinglist", response_model=ShoppingList, tags=["Menu"], status_code=status.HTTP_202_ACCEPTED)
async def change_item_in_shopping_list(data : ItemUpdate, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return update_item_data(data=data, db_session=db, user=user)

@router.delete("/menu/shoppinglist/item/{item_id}", response_model=None, tags=["Menu"], status_code=status.HTTP_202_ACCEPTED)
async def delete_item(item_id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return delete_shoppinglist_item(id=item_id, db_session=db, user=user)

@router.delete("/menu/shoppinglist/{id}", response_model=None, tags=["Menu"], status_code=status.HTTP_202_ACCEPTED)
async def delete_item(id : int, db : Session = Depends(get_db), user : User = Depends(authenticate)):
    return delete_shopping_list_from_db(id=id, db_session=db, user=user)