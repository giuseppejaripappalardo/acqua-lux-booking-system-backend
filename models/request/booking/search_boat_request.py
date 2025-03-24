from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SearchBoatRequest(BaseModel):
    seat: int
    start_date: datetime
    end_date: datetime
    model_config = ConfigDict(from_attributes=True)
