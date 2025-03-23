from models.response.boat.boat_response import BoatResponse
from models.response.booking.booking_response import BookingResponse


class BookingWithBoatResponse(BookingResponse):
    boat: BoatResponse