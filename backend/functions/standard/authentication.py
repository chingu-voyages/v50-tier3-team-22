from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
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

from functions.db.db_user import create_user, delete_user, get_user_by_username, get_user_by_email
from functions.db.db_recipe import delete_recipes

CREDENTIAL_EXEPTION = HTTPException(status_code=401, detail="Could not validate the credential")
INCORRECT_LOGIN_EXEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"},)

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Token and verification functions
def verify_password(password:str, salt:str, hashed_password:str):
    return pwd_context.verify(password + salt, hashed_password)
    

def login_for_access(db_session:Session, data:LoginUser):
    if len(re.findall(pattern="[^a-z0-9]", string=data.username)) > 0 or len(data.username) < 4:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username is not acceptable")
    
    if len(data.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")
    #validate input

    user = get_user_by_username(db=db_session,username=data.username)

    if user == None:
        raise INCORRECT_LOGIN_EXEPTION
    #check if user exists and retrieve user

    if not verify_password(password=data.password, salt=user.salt, hashed_password=user.password):
        raise INCORRECT_LOGIN_EXEPTION
    
    #verify password

    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub" : user.username, "expires" : expires.isoformat()}

    #generate expiration time and sub for ecnoding

    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    #generate and return access token
    
    return TokenReturn(access_token=access_token, token_type="bearer", expiry=expires)


def authenticate(db_session:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires : datetime = datetime.fromisoformat(payload.get("expires"))
        username : str | None = payload.get("sub")
    except InvalidTokenError:
        raise credentials_exception
    #verify token 
    if username is None:
        raise credentials_exception
    user = get_user_by_username(db=db_session,username=username)

    if user == None:
        raise credentials_exception
    elif datetime.now(UTC) > expires:
        raise credentials_exception
    #check if sub info is valid and if expired
    print(user.recipes)
    user_out = User(**user.__dict__)

    #return the user
    return user_out


#User functions
def make_new_user(data:RegisterUser, db_session : Session):
    if len(re.findall(pattern="[^a-z0-9]", string=data.username)) > 0 or len(data.username) < 4:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username is not acceptable")
    
    if re.fullmatch(pattern="[a-z0-9/.]+@[a-z0-9/]+\.[a-z]+", string=data.email) == None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email address")
    
    if len(data.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")

    #Validate the user input to make sure the data is correct
    

    if get_user_by_username(db=db_session, username=data.username) != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail = "Username is already taken"
        )
    elif get_user_by_email(db=db_session, email=data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail = "This email is already used"
        )

    #Checking the data base for conflicts
    salt = str(gensalt())
    hashed_password = pwd_context.hash(data.password + salt)
    user = CreateUser(
        username = data.username,
        email = data.email,
        salt = salt,
        password = hashed_password
    )
   

    #Generating salt and hashing pw
    
    user = create_user(db=db_session, user=user)
    #Adding the user to the database
    user_out = User(**user.__dict__, recipes=[])
  
    #Formulate response
    return user_out

def remove_user(db_session:Session, user:User, data:LoginUser):
    if len(re.findall(pattern="[^a-z0-9]", string=data.username)) > 0 or len(data.username) < 4:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username is not acceptable")
    
    if len(data.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")


    #Validate login data

    user = get_user_by_username(db=db_session, username=data.username)

    if user == None:
        raise INCORRECT_LOGIN_EXEPTION
    elif not verify_password(data.password, user.salt, user.password):
        raise INCORRECT_LOGIN_EXEPTION
    #Double authenticate
    
    delete_recipes(db=db_session, owner_id=user.id)
    delete_user(db=db_session,id=user.id)
    #remove user and recipes
    return
    #return