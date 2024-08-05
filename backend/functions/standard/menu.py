from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, date

from database.schemas.authentication import User

from functions.db.db_day import create_day, get_day_by_id, get_day_by_date, update_day, delete_day
from functions.db.db_menu import create_menu, get_menu_by_start_date, update_menu, delete_menu
from functions.db.db_recipe import get_recipe_by_id

from database.schemas.day import CreateDay, DayBase, DB_Day
from database.schemas.menu import CreateMenu, FullMenu
from database.schemas.recipes import RecipeId, Recipe
from database.schemas.ingredients import FullIngredient	

VALIDATION_ERROR = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "The data sent is invalid"
    )

MEAL_PLAN_OPTIONS = ["breakfast", "snacks", "lunch", "dinner"] 

def get_week_start(date : date) -> date:
    """Finds the date for the first day of the week"""
    day_from_monday = int(date.strftime("%w")) - 1  
    if day_from_monday == -1:
        day_from_monday = 6  
    day_from_monday = timedelta(days=day_from_monday)
    #finding the day to subtract from the date to get the first day of the month
    week_start = date - day_from_monday
    
    return week_start


def add_recipe_to_menu(meal : str, data : DayBase, recipe_id : RecipeId, db_session : Session, user : User):
    if meal not in MEAL_PLAN_OPTIONS:
        raise VALIDATION_ERROR
    #validate meal 
    recipe : Recipe | None = get_recipe_by_id(db=db_session, id=recipe_id.id)
    if recipe == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe with this id was not found"
        )
    elif recipe.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to access this recipe"
        )

    #validate recipe id
    week_start = get_week_start(date=data.date)
    
    menu = get_menu_by_start_date(db=db_session, date=week_start, owner_id=user.id)
   

    day = None
    if menu != None:
        if menu.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unauthorized to access this menu"
            )
        
    #Check for ownership if menu exists 
        day = get_day_by_date(db=db_session, date=data.date, menu_id=menu.id)
    else:
        week_end = week_start + timedelta(days=6)
        menu_data = CreateMenu(
            start_date=week_start, 
            end_date=week_end,
            owner_id=user.id    
        )
        menu = create_menu(db=db_session, menu=menu_data)
    
    if day == None:
        day = create_day(db=db_session, day=CreateDay(
            date=data.date,
            name=data.date.strftime("%A"),
            menu_id=menu.id
        ))
    #checking the availability of day and menu and create the ones that dont exists

    data_to_update = day.meal_plan
    data_to_update[meal].append(recipe.id)
    
    update_day(db=db_session, id=day.id, data_to_update={"meal_plan" : data_to_update})
    day = get_day_by_id(db=db_session, id=day.id)
    #creating the data to update and update the day
    meal_plan : dict = day.meal_plan
   
    day_to_return = DB_Day(**day.dict())

    for key, value in meal_plan.items():
        recipe_list = []
        for recipe_id in value:
            recipe : Recipe = get_recipe_by_id(db=db_session, id = recipe_id)
            recipe_list.append(recipe)
        meal_plan[key] = recipe_list

    day_to_return.meal_plan = meal_plan

    #fetching the recipes to return with day     
    
    return day_to_return

def delete_recipe_from_menu(meal : str, date : date, recipe_id : RecipeId, db_session : Session, user : User):
    if meal not in MEAL_PLAN_OPTIONS:
        raise VALIDATION_ERROR
    #validate imput
    
    week_start = get_week_start(date=date)

    menu = get_menu_by_start_date(db=db_session, date=week_start, owner_id=user.id)

    if menu == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu for this user with this date was not found"
        )
    
    day = get_day_by_date(db=db_session, date=date, menu_id=menu.id)

    if day == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no meal plan for this user on this day"
        )
    #find menu and day and authenticate
    if recipe_id.id not in day.meal_plan[meal]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This recipe is not on the daily menu"
        )

    #check if the recipe is on the menu

    new_recipe_list : list = day.meal_plan[meal]
    new_recipe_list.remove(recipe_id.id)

    day.meal_plan[meal] = new_recipe_list

    update_day(db=db_session, id=day.id, data_to_update={"meal_plan" : day.meal_plan})

    day = get_day_by_id(db=db_session, id=day.id)
    #delete the recipe from the menu
    if day.meal_plan == {"breakfast" : [], "lunch" : [], "dinner" : [], "snacks" : []}:
        delete_day(db=db_session, id=day.id)

    menu = get_menu_by_start_date(db=db_session, date=week_start, owner_id=user.id)

    if len(menu.days) == 0:
        delete_menu(db=db_session, id=menu.id)

    #delete day if no meal plan
    return 


def get_weekly_menu(date : date, db_session : Session, user : User):
    week_start = get_week_start(date=date)
    menu = get_menu_by_start_date(db=db_session, date=week_start, owner_id=user.id)
    #get the menu object

    if menu == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu was not yet created"
        )

    menu = FullMenu(**menu.dict(), days=menu.days)
    return menu

'''
shopping_list : dict = menu.ingredients

    for ingredient in recipe.ingredients:
        ingredient = FullIngredient(**ingredient, owner_id=user.id)
        if str(ingredient.id) not in shopping_list.keys():
            shopping_list[str(ingredient.id)] = {ingredient.unit : {
                "amount" : ingredient.amount, 
                "type" : ingredient.type, 
                "name" : ingredient.name
            }}
        elif str(ingredient.unit) not in shopping_list[str(ingredient.id)].keys():
            shopping_list[str(ingredient.id)][str(ingredient.unit)] =  {
                "amount" : ingredient.amount, 
                "type" : ingredient.type, 
                "name" : ingredient.name
            }
        else:
            shopping_list[str(ingredient.id)][str(ingredient.unit)]["amount"] = shopping_list[str(ingredient.id)][str(ingredient.unit)]["amount"] + ingredient.amount

    update_menu(db=db_session, id=menu.id, data_to_update={"ingredients" : shopping_list})

    #adding ingredients to the weekly menu

'''