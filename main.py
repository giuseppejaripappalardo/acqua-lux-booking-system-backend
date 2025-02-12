import os

from fastapi import FastAPI

from config.database import Database
from controllers import user

app = FastAPI()

"""
Utilizzato solo in ambiente di development
lo scopo è quello di inizializzare il database
in particolare la classe Database chiamando questa istruzione
Base.metadata.create_all(bind=self.engine) fa si che SQLAlchemy
vada a creare gli schema nel database a partire dai modelli presenti
nella cartella models
"""
if os.getenv("ENVIRONMENT_NAME") == "dev":
    database = Database()

# Includo i controllers, questo ci consente di esporre i servizi previsti dal backend.
app.include_router(user.router)