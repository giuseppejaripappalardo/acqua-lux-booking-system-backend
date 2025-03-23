from typing import Optional

from pydantic import ConfigDict

from models.response.boat.boat_response import BoatResponse
from models.response.booking.booking_response import BookingResponse


class BoatWithBookingsResponse(BoatResponse):
    bookings: Optional[list[BookingResponse]] = None
    model_config = ConfigDict(from_attributes=True)