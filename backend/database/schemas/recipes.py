from pydantic import BaseModel
from fastapi import Form
from typing import Optional

class RecipeBase(BaseModel):
    """"The base for other schemas and needed info from the user for creation"""
    name : str
    description : str
    cuisine : str | None = None
    category : int
    time : int
    level : int
    

class RecipeCreate(RecipeBase):
    """Information needed to create a db modell"""
    image_name : str | None = None
    owner_id : int

class Recipe(RecipeBase):
    """Full recipe schema"""
    id : int
    owner_id : int
    image_url : str = None
    class Config:
        orm_mode = True

class UpdateRecipeData(BaseModel):
    """"The schema used to update and existing recipe"""
    name : str = None
    description : str = None
    cuisine : str = None
    category : int = None
    time : int = None
    level : int = None

class CreateRecipeForm:
    def __init__(
        self,
        name : str = Form(),
        description : str = Form(),
        cuisine : str = Form(None),
        category : int = Form(),
        time : int = Form(),
        level : int = Form(),
    ): 
        self.name = name
        self.description = description
        self.cuisine = cuisine
        self.category = category
        self.time = time
        self.level = level

    def get_recipe_base(self) -> RecipeBase:
        return RecipeBase(**self.__dict__)
    

class  UpdateRecipeForm:
    def __init__(
        self,
        name : Optional[str] = Form(None),
        description : Optional[str] = Form(None),
        cuisine : Optional[str] = Form(None),
        category : Optional[int] = Form(None),
        time : Optional[int] = Form(None),
        level : Optional[int] = Form(None),
        
    ): 
        self.name = name
        self.description = description
        self.cuisine = cuisine
        self.category = category
        self.time = time
        self.level = level

    def get_recipe_base(self) -> RecipeBase:
        return UpdateRecipeData(**self.__dict__)