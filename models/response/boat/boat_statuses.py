from pydantic import ConfigDict, BaseModel


class BoatStatusesResponse(BaseModel):
    id: int
    name: str
    description: str
    model_config = ConfigDict(from_attributes=True)