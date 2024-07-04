from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.schemas.authentication import User, LoginUser, UserAuth

CREDENTIAL_EXEPTION = HTTPException(status_code=401, detail="Could not validate the credential")

def create_user(user:LoginUser, db_session : Session):
    
    #Validate the user imput to make sure the data is correct

    #Checking the data base for conflicts

    #Generating salt

    #Adding the user to the database


    #Formulate response

    pass