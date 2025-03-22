import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from utils.logger_service import LoggerService


class Database:
    engine = None
    session_local = None
    _instance = None
    _logger = LoggerService().logger
    _initialized = False

    def __new__(cls):
        """
            Uso il pattern singleton per assicurarmi di avere una sola istanza
            del database.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        """
            Genero la stringa di connessione al db leggendo le variabili
            d'ambiente appositamente previste.
        """
        database_url = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        """
            In questo step usiamo la stringa di connessione al db per creare engine
        """
        self.engine = create_engine(database_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._initialized = True

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()
