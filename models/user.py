from sqlalchemy import Column, Integer, String, DateTime, func

from models import Base


# Definisco lo schema di base
class User(Base):
    # Qui indichiamo che questo modello è linkato con la tabella users.
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), index=True, nullable=False, unique=True)
    password = Column(String(255), index=True, nullable=False)
    firstname = Column(String(255), index=True, nullable=False)
    lastname = Column(String(255), index=True, nullable=False)
    role_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)