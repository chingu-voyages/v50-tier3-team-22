from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database_services import get_db

from database.schemas.authentication import User, RegisterUser, LoginUser, TokenReturn

from functions.standard.authentication import make_new_user, login_for_access

router = APIRouter()

@router.post("/token", response_model=TokenReturn, tags=["Auth"], status_code=status.HTTP_201_CREATED)
async def create_auth_token(db : Session = Depends(get_db), form_data : OAuth2PasswordRequestForm = Depends()):
    return login_for_access(db_session=db, data=LoginUser(username=form_data.username, password=form_data.password))


@router.post("/register", response_model=User, tags=["Auth"], status_code=status.HTTP_201_CREATED)
async def register_user(data:RegisterUser, db:Session = Depends(get_db)):
    return make_new_user(data=data, db_session=db)