from fastapi import HTTPException, Depends, status, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from database.database_services import get_db

import re
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, UTC
from os import getenv
from bcrypt import gensalt
from passlib.context import CryptContext
from database.schemas.authentication import User, LoginUser, TokenReturn, RegisterUser, CreateUser

from functions.db.db_user import create_user, delete_user, get_user_by_email
from functions.db.db_recipe import delete_recipes, get_recipes_by_user, update_recipe
from functions.db.db_ingredients import delete_ingredients
from functions.db.db_day import delete_days
from functions.db.db_menu import delete_menus
from functions.db.db_item import delete_items
from functions.db.db_shoppingls import delete_shopping_lists
from functions.standard.image_manager import delete_image

CREDENTIAL_EXEPTION = HTTPException(status_code=401, detail="Could not validate the credential")
INCORRECT_LOGIN_EXEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",headers={"WWW-Authenticate": "Bearer"},)

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

token_key = APIKeyHeader(name="Authorization")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Token and verification functions
def verify_password(password:str, salt:str, hashed_password:str):
    return pwd_context.verify(password + salt, hashed_password)
    

def login_for_access(db_session:Session, data:LoginUser):
    if re.fullmatch(pattern="[a-z0-9/.]+@[a-z0-9/]+\.[a-z]+", string=data.email) == None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email address")
    
    if len(data.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")
    #validate input
    user = get_user_by_email(db=db_session, email=data.email)
    
    if user == None:
        raise INCORRECT_LOGIN_EXEPTION
    #check if user exists and retrieve user

    if not verify_password(password=data.password, salt=user.salt, hashed_password=user.password):
        raise INCORRECT_LOGIN_EXEPTION
    
    #verify password

    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub" : user.email, "expires" : expires.isoformat()}

    #generate expiration time and sub for ecnoding

    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    #generate and return access token
    
    return TokenReturn(access_token=access_token, token_type="bearer", expiry=expires)


def authenticate(db_session:Session = Depends(get_db), auth_key: str = Security(token_key)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    auth = auth_key.split(" ")
    token_type = auth[0]
    if token_type != "Bearer":
        raise credentials_exception
    
    token = auth[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires : datetime = datetime.fromisoformat(payload.get("expires"))
        email : str | None = payload.get("sub")

    except InvalidTokenError:
        raise credentials_exception
    #verify token 
    if email is None:
        raise credentials_exception
    user = get_user_by_email(db=db_session, email=email)

    if user == None:
        raise credentials_exception
    elif datetime.now(UTC) > expires:
        raise credentials_exception
    #check if sub info is valid and if expired

    user_out = user.dict()
    user_out["recipes"] = user.recipes
    user_out["menus"] = user.menus
    user_out["shopping_lists"] = user.shopping_lists

    #return the user
    return User(**user_out)


#User functions
def make_new_user(data:RegisterUser, db_session : Session):
    if re.fullmatch(pattern="[a-z0-9/.]+@[a-z0-9/]+\.[a-z]+", string=data.email) == None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email address")
    
    if len(re.findall(pattern="[^a-zA-z ]", string=data.name)) > 0 or len(data.name) < 4:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid name provided please do not use special characters")
    
    if len(data.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")

    #Validate the user input to make sure the data is correct
    

    if get_user_by_email(db=db_session, email=data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail = "This email is already used"
        )

    #Checking the data base for conflicts
    salt = str(gensalt())
    hashed_password = pwd_context.hash(data.password + salt)
    user = CreateUser(
        name = data.name,
        email = data.email,
        salt = salt,
        password = hashed_password
    )
   

    #Generating salt and hashing pw
    
    user = create_user(db=db_session, user=user)
    #Adding the user to the database

    user_out = User(recipes=[], menus=[],**user.dict())
  
    #Formulate response
    return user_out

def remove_user(db_session:Session, user:User, data:LoginUser):
    if re.fullmatch(pattern="[a-z0-9/.]+@[a-z0-9/]+\.[a-z]+", string=data.email) == None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email address")

    if len(data.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")


    #Validate login data

    user = get_user_by_email(db=db_session, email=data.email)

    if user == None:
        raise INCORRECT_LOGIN_EXEPTION
    elif not verify_password(data.password, user.salt, user.password):
        raise INCORRECT_LOGIN_EXEPTION
    #Double authenticate
    
    recipes = get_recipes_by_user(db=db_session, owner_id=user.id)
    for recipe in recipes:
        if recipe.image_name != None:
            delete_image(recipe.image_name)
            update_recipe(db=db_session, id=recipe.id, data_to_update={"image_name" : None})
    #Delete images

    delete_recipes(db=db_session, owner_id=user.id)
    delete_ingredients(db=db_session, owner_id=user.id)
    for menu in user.menus:
        delete_days(db=db_session, menu_id=menu.id)
    delete_menus(db=db_session, owner_id=user.id)
    for shopping_list in user.shopping_lists:
        delete_items(db=db_session, shopping_list_id=shopping_list.id)
    delete_shopping_lists(db=db_session, owner_id=user.id)
    delete_user(db=db_session,id=user.id)
    #remove user, recipes, ingredients, menus, and days
    return
    #return
