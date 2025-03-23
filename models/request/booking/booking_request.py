from decimal import Decimal

from models.request.booking.search_boat_request import SearchBoatRequest
from utils.enum.booking_statuses import BookingStatuses
from utils.enum.payment_methods import PaymentMethods


class CustomerBookingRequest(SearchBoatRequest):
    boat_id: int
    notes: str
    payment_method: PaymentMethods

class BookingRequest(CustomerBookingRequest):
    customer_id: int
    reservation_code: str
    reservation_status: BookingStatuses
    total_price: Decimal