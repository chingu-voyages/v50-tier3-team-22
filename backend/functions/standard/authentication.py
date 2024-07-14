from fastapi import HTTPException, Depends, status, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from database.database_services import get_db

import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, UTC
from os import getenv
from bcrypt import gensalt
from passlib.context import CryptContext
from database.schemas.authentication import User, LoginUser, TokenReturn, RegisterUser
from database.models.user import User as DbUser

from functions.db.db_user import create_user, delete_user, get_user_by_email

CREDENTIAL_EXEPTION = HTTPException(status_code=401, detail="Could not validate the credential")
INCORRECT_LOGIN_EXEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"},)

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

token_key = APIKeyHeader(name="Authorization")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Token and verification functions
def verify_password(password:str, salt:str, hashed_password:str):
    return pwd_context.verify(password + salt, hashed_password)

def login_for_access(db_session:Session, data:LoginUser):
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
    print(auth_key)
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
        email : str = payload.get("sub")
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
    user_out = User(
        id=user.id,
        name=user.name,
        email=user.email
    )

    #return the user
    return user_out


#User functions
def make_new_user(data:RegisterUser, db_session : Session):
    user = DbUser(
        name = data.name,
        email = data.email
    )
    

    #Validate the user input to make sure the data is correct
    
    if get_user_by_email(db=db_session, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail = "This email is already used"
        )

    #Checking the data base for conflicts

    user.salt = str(gensalt())
    user.password = pwd_context.hash(data.password + user.salt)

    #Generating salt and hashing pw
    
    user = create_user(db=db_session,user=user)
    
    #Adding the user to the database

    user_out = User(
        id=user.id,
        name=user.name,
        email=user.email
    )
  
    #Formulate response
    return user_out

def remove_user(db_session:Session, user:User, data:LoginUser):
    
    #Validate login data

    user = get_user_by_email(db=db_session, email=data.email)

    if user == None:
        raise INCORRECT_LOGIN_EXEPTION
    elif not verify_password(data.password, user.salt, user.password):
        raise INCORRECT_LOGIN_EXEPTION
    #Double authenticate

    delete_user(db=db_session,id=user.id)
    #remove user
    return
    #return