from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

router = APIRouter()

@router.post("/recipe", tags=["Recipe"], status_code=status.HTTP_201_CREATED)
async def create_new_recipe():
    return