from urllib.parse import quote_plus

from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Carico dotenv, mi serve per poter leggere le variabili d'ambiente
# Che ho definito nel file .env. Questo può essere molto utile nel caso
# in ottica futura volessi utilizzare un container docker
# Ci consente di injettare il file .env evitando di doverlo prevedere tra i file di progetto!
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Qui creo l'engine cosi da poter creare la sessione
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()