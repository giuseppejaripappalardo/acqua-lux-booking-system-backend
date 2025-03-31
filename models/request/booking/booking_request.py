from datetime import datetime

from pydantic import BaseModel

from models.request.booking.booking_delete_request import BookingDeleteRequest
from models.request.booking.search_boat_request import SearchBoatRequest
from utils.enum.payment_methods import PaymentMethods


class CustomerBookingRequest(SearchBoatRequest):
    boat_id: int
    notes: str
    payment_method: PaymentMethods

class EditBookingRequest(BaseModel):
    booking_id: int
    start_date: datetime
    end_date: datetime
    boat_id: int
    payment_method: PaymentMethods
    notes: str
    seat: int

class GetBookingByIdRequest(BookingDeleteRequest):
    pass