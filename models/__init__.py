from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Importa i modelli
from .user import User