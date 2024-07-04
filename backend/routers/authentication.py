from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database_services import get_db

from database.schemas.authentication import User, LoginUser, Token

from functions.standard.authentication import create_user

router = APIRouter()

@router.post("/sign_up", tags=["Auth"], status_code=201)
async def register_user(user:LoginUser, db:Session = Depends(get_db)):
    return create_user(user=user, db_session=db)