from datetime import datetime

from pydantic import BaseModel


class BookingRequest(BaseModel):
    seat_number: int
    start_date: datetime
    end_date: datetime