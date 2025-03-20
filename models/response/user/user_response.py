from pydantic import ConfigDict, BaseModel

class UserResponse(BaseModel):
    """
        Ho creato un DTO specifico per la response con lo scopo di evitare
        di esporre dati sensibili come ad esempio la password, che di fatto viene
        esclusa perchè estendiamo solo BaseUser che non contiene il campo password di base.
    """
    id: int
    username: str
    firstname: str
    lastname: str
    role_id: int

    model_config = ConfigDict(from_attributes=True)