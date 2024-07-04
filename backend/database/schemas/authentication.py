from pydantic import BaseModel

class UserBase(BaseModel):
    """Class with the basic info needed for all user shemas"""
    username : str
    email : str

class User(UserBase):
    """Basic user modell sterilized of secrets"""
    id : int

class LoginUser(UserBase):
    """User modell for login/register the user"""
    password : str

class CreateUser(LoginUser):
    salt : str

class UserAuth(LoginUser):
    """All necessary information for authentication"""
    id : str
    salt : str

class Token(BaseModel):
    """"Token modell"""
    access_token : str
    token_type : str

class TokenReturn(Token):
    """Token modell containing expiry"""
    expiry_min : int