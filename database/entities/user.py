from sqlalchemy import Column, Integer, String, DateTime, func

from database.entities import Base


# Definisco lo schema di base
class User(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
        specifichiamo anche il nome della tabella di riferimento che in questo caso è
        users.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), index=True, nullable=False, unique=True)
    password = Column(String(255), index=True, nullable=False)
    firstname = Column(String(255), index=True, nullable=False)
    lastname = Column(String(255), index=True, nullable=False)
    role_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)