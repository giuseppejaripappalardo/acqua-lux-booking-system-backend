from pydantic import ConfigDict, BaseModel

from models.response.role.role_response import RoleResponse


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
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)