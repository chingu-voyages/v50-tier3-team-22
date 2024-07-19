from pydantic import BaseModel
from datetime import datetime
from database.schemas.recipes import Recipe
class UserBase(BaseModel):
    """Class with the basic info needed for all user shemas"""
    name : str
    email : str

class User(UserBase):
    """Basic user model sterilized of secrets"""
    id : int
    recipes : list[Recipe]

class LoginUser(BaseModel):
    """User model for login"""
    email : str
    password : str

class RegisterUser(UserBase):
    """User model for regitering"""
    password : str
class CreateUser(RegisterUser):
    salt : str
    

class Token(BaseModel):
    """"Token model"""
    access_token : str
    token_type : str

class TokenReturn(Token):
    """Token model containing expiry"""
    expiry : datetime