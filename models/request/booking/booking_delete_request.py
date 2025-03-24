from pydantic import BaseModel


class BookingDeleteRequest(BaseModel):
    booking_id: int

