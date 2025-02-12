import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import Base
from utils.logger import Logger


class Database:

    engine = None
    session_local = None
    env = os.getenv("ENVIRONMENT_NAME", "dev")
    _instance = None
    _logger = Logger().logger
    _initialized = False

    """
    Evitiamo di ricreare l'istanza del database più volte.
    Se già questa classe è stata istanziata ritorniamo la stessa
    istanza. Qui sfruttiamo volutamente il pattern singleton.
    """
    def __new__(cls):
        cls._logger.info("Creating Database instance")
        if cls._instance is None:
            cls._logger.info("Istanza è None quindi la creo")
            cls._instance = super().__new__(cls)
        else:
            cls._logger.info("l'istanza esiste già, la ritorno ;)")
        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        """
        Qui sto creando la stringa di connessione da passare
        per la connessione al database
        """
        DATABASE_URL = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        """
            A questo punto utilizziamo la stringa di connessione al db
            per creare l'engine e la sessione'
        """
        self.engine = create_engine(DATABASE_URL)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        if self.env == "dev":
            Base.metadata.create_all(bind=self.engine)

        self._initialized = True

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()
