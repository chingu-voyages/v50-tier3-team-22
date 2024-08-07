from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime, UTC

from database.schemas.authentication import User

from functions.db.db_day import create_day, get_day_by_id, get_day_by_date, update_day, delete_day
from functions.db.db_menu import create_menu, get_menu_by_start_date, delete_menu, get_menu_by_id
from functions.db.db_recipe import get_recipe_by_id
from functions.db.db_shoppingls import get_shoppig_list_of_menu, create_shopping_list, get_shopping_list_by_id, delete_shopping_list
from functions.db.db_item import create_item, update_item, get_item_by_id, delete_item, delete_items

from database.schemas.day import CreateDay, DayBase, DB_Day
from database.schemas.menu import CreateMenu, FullMenu
from database.schemas.recipes import RecipeId, Recipe
from database.schemas.ingredients import FullIngredient	
from database.schemas.shoppingls import ShoppingListBase, ShoppingList
from database.schemas.item import ItemBase, ItemUpdate

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

def generate_shopping_list(menu_id : int, generate_new : bool, db_session : Session, user : User):
    menu = get_menu_by_id(db=db_session, id=menu_id)
    if menu == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu with this id was not found"
        )
    elif menu.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot access this menu"
        )
    #authorizing the user to access this menu and validationg the id
    shopping_lists = get_shoppig_list_of_menu(db=db_session,menu_id=menu_id)
    #check if there is previous shopping list
    if len(shopping_lists) > 0 and generate_new == False:
        return shopping_lists

    days : list[DB_Day] = menu.days

    recipe_ids = []
    for day in days:
        for ids in day.meal_plan.values():
            recipe_ids += ids
    #fetching all the recipe ids in the menu
    shopping_list = {}
    previous_recipe_id = 0
    for recipe_id in recipe_ids:
        #looping through the recipe ids in the menu

        if previous_recipe_id == recipe_id:
            pass
        #passing over if the previous recipe id is the same as it is already handeled

        else:
            previous_recipe_id = recipe_id
            recipe_ocurence = recipe_ids.count(recipe_id)
            #used later to multiply how many times recipe ocures and add the amount

            recipe = get_recipe_by_id(db=db_session, id=recipe_id)
            #fetching recipe

            for ingredient in recipe.ingredients:
                #looping throuhg the ingredients
                ingredient = FullIngredient(**ingredient, owner_id=user.id)
            
                if (str(ingredient.id) not in shopping_list.keys()):
                    #adding the ingredient id if its not yet present in the shopping list
                    shopping_list[str(ingredient.id)] = {str(ingredient.unit) : {
                        "amount" : ingredient.amount * recipe_ocurence, 
                        "type" : ingredient.type, 
                        "name" : ingredient.name
                    }}
                elif str(ingredient.unit) not in shopping_list[str(ingredient.id)].keys():
                    #adding the new unit to the ingredient if it is not yet present in the shopping list
                    shopping_list[str(ingredient.id)][str(ingredient.unit)] =  {
                        "amount" : ingredient.amount * recipe_ocurence, 
                        "type" : ingredient.type, 
                        "name" : ingredient.name
                    }
                else:
                    #adding the amount if it is already present with unit and id
                    shopping_list[str(ingredient.id)][str(ingredient.unit)]["amount"] += ingredient.amount * recipe_ocurence
    #generated shopping list as a dictionary
    db_shopping_list = ShoppingListBase(menu_id=menu_id, created=datetime.now(UTC), owner_id=user.id)
    db_shopping_list = create_shopping_list(db=db_session, shopping_list=db_shopping_list)

    #generating shopping list to db
    for ingredient_id in shopping_list:
        for ingredient_unit in shopping_list[ingredient_id]:
            item = ItemBase(**shopping_list[ingredient_id][ingredient_unit], unit=ingredient_unit, shopping_list_id=db_shopping_list.id)
            create_item(db=db_session, item=item)

    #filling creating shopping list items to database
    shopping_list = get_shopping_list_by_id(db=db_session, id=db_shopping_list.id)
    #retribing shopping list

    return ShoppingList(**shopping_list.dict(), items=shopping_list.items)

def get_shopping_list_from_db(id : int, db_session : Session, user : User):
    shopping_list = get_shopping_list_by_id(db=db_session, id=id)

    if shopping_list == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list with this id was not found "
        )
    elif shopping_list.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this shopping list"
        )
    #validate input

    return ShoppingList(**shopping_list.dict(), items=shopping_list.items)
    #return the shopping list


def update_item_data(data : ItemUpdate, db_session : Session, user : User):
    item = get_item_by_id(db=db_session, id=data.id)
    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item with this id was not found"
        )
    
    shopping_list = get_shopping_list_by_id(db=db_session, id=item.shopping_list_id)
    if shopping_list.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this shopping list item"
        )
    #get the item to update and check access
    data_to_update = {}

    if data.amount != None:
        data_to_update["amount"] = data.amount
    
    if data.name != None:
        data_to_update["name"] = data.name

    if data.unit != None:
        data_to_update["unit"] = data.unit

    if data.is_checked != None:
        data_to_update["is_checked"] = data.is_checked
    #create data to update

    if len(data_to_update.keys()) == 0:
        raise VALIDATION_ERROR

    update_item(db=db_session, data_to_update=data_to_update, id=data.id)

    shopping_list = get_shopping_list_by_id(db=db_session, id=shopping_list.id)

    return ShoppingList(**shopping_list.dict(), items=shopping_list.items)
    #update and return

def delete_shoppinglist_item(id : int, db_session : Session, user : User):
    item = get_item_by_id(db=db_session, id=id)
    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item with this id was not found"
        )
    
    shopping_list = get_shopping_list_by_id(db=db_session, id=item.shopping_list_id)
    if shopping_list.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this shopping list item"
        )
    #get the item to update and check access

    delete_item(db=db_session, id=id)
    #delete shopping list item
    return

def delete_shopping_list_from_db(id : int, db_session : Session, user : User):
    shopping_list = get_shopping_list_by_id(db=db_session, id=id)

    if shopping_list == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list with this id was not found "
        )
    elif shopping_list.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this shopping list"
        )
    #validate and check

    delete_items(db=db_session, shopping_list_id=id)
    delete_shopping_list(db=db_session, id=id)

    return