from pydantic import BaseModel, ConfigDict


class UserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    """
        DTO per la registrazione di un nuovo utente
        In questo caso includiamo ovviamente la password
        per la registrazione
    """
    username: str
    firstname: str
    lastname: str
    role_id: int
    password: str