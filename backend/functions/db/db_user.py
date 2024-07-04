from sqlalchemy.orm import Session

import database.modells.user as user_modell
from database.schemas.authentication import UserAuth

def create_user(db:Session, user):
    pass