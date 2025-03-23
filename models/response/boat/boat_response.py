from decimal import Decimal

from pydantic import ConfigDict, BaseModel

from models.response.boat.boat_statuses import BoatStatusesResponse


class BoatResponse(BaseModel):
    id: int
    name: str
    description: str
    seat: int
    price_per_hour: Decimal
    location: str
    boat_status: BoatStatusesResponse
    model_config = ConfigDict(from_attributes=True)