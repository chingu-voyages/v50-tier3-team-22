from pydantic import BaseModel

class RecipeBase(BaseModel):
    """"The base for other schemas and needed info from the user for creation"""
    name : str
    description : str
    guide : str

class RecipeCreate(RecipeBase):
    """Information needed to create a db modell"""
    owner_id : int

class Recipe(RecipeCreate):
    """Full recipe schema"""
    id : int

    class Config:
        orm_mode = True

class UpdateRecipeData(BaseModel):
    """"The schema used to update and existing recipe"""
    name : str = None
    description : str = None
    guide : str = None