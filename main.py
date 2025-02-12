import logging
import os
import traceback
from urllib.parse import quote_plus

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine

from routers import user
from config.database import engine
from models import Base

# Abilitare il logging dettagliato
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?connect_timeout=10"
try:
    logging.info("Provo a connettermi al database...")
    logging.info(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    logging.info("Connessione al database riuscita.")

    logging.info("Provo a creare le tabelle...")
    Base.metadata.create_all(bind=engine)
    logging.info("Tabelle create con successo.")
    connection.close()
except Exception as e:
    logging.error("Errore durante la connessione o la creazione delle tabelle:")
    logging.error(traceback.format_exc())

app = FastAPI()
logging.info("Inizio l'app")

# utilizzato solo per scopo di creazione tabelle in dev.
# TODO inserire condizione per verificare se env è prod o debug.
try:
    logging.info("Provo a creare le tabelle...")
    Base.metadata.create_all(bind=engine)
    logging.info("Tabelle create con successo.")
except Exception as e:
    logging.error("Errore nella creazione delle tabelle:")
    logging.error(traceback.format_exc())  # Mostra il traceback completo

logging.info("fine inizio app")

# Includo i routers, questo ci consente di esporre i servizi previsti dal backend.
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Benvenuto/a in AcquaLux API"}