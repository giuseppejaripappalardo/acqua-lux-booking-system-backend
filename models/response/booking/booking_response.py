from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.response.user.user_response import UserResponse
from utils.enum.booking_statuses import BookingStatuses
from utils.enum.payment_methods import PaymentMethods


class BookingResponse(BaseModel):
    id: int
    seat: int
    start_date: datetime
    end_date: datetime
    boat_id: int
    customer_id: int
    notes: str
    total_price: Decimal
    reservation_code: str
    payment_method: PaymentMethods
    reservation_status: BookingStatuses
    created_at: datetime
    modified_at: datetime
    customer: UserResponse
    model_config = ConfigDict(from_attributes=True)