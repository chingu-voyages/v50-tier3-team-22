from sqlalchemy.orm import Session

from database.modells.user import User as UserModell
from database.schemas.authentication import CreateUser

def create_user(db : Session, user : CreateUser) -> UserModell:
    db_user = UserModell(
        username = user.username,
        password = user.password,
        salt = user.salt,
        email = user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_username(db : Session, username : str) -> UserModell:
    return db.query(UserModell).filter(UserModell.username == username).first()

def get_user_by_id(db : Session, user_id : int) -> UserModell:
    return db.query(UserModell).filter(UserModell.id == user_id).first()

def get_user_by_email(db : Session, email : str) -> UserModell:
    return db.query(UserModell).filter(UserModell.email == email).first()