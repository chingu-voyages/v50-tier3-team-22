from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database.database_services import get_db, start_database

import routers.authentication as authentication
import routers.recipes as recipes

start_database()

app = FastAPI()

app.include_router(authentication.router)
app.include_router(recipes.router)

@app.get("/")
def root():
    return RedirectResponse("/docs")

