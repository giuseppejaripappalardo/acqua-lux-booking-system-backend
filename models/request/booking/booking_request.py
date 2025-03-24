from datetime import datetime

from models.request.booking.search_boat_request import SearchBoatRequest
from utils.enum.payment_methods import PaymentMethods


class CustomerBookingRequest(SearchBoatRequest):
    boat_id: int
    notes: str
    payment_method: PaymentMethods

class EditBookingRequest(CustomerBookingRequest):
    edit_start_date: datetime
    edit_end_date: datetime