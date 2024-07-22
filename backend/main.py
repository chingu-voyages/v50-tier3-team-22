from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from database.database_services import start_database

import routers.authentication as authentication
import routers.recipes as recipes
import routers.ingredients as ingredients

start_database()

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://web-v50-tier3-team-22.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(recipes.router)
app.include_router(ingredients.router)


@app.get("/")
def root():
    return RedirectResponse("/docs")

