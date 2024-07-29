from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database_services import get_db

from functions.standard.authentication import authenticate
from database.schemas.authentication import User

router = APIRouter()

@router.get("/menu/day/options", response_model=dict, tags=["Menu"], status_code=status.HTTP_200_OK)
async def get_options():
    return