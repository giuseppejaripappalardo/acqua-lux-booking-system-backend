import os

from fastapi import FastAPI
from routes.users import router as users_router

app = FastAPI()

"""
    Esponiamo le routes dei controller previsti
    dal project work.
"""
app.include_router(users_router)