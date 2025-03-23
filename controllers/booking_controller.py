from fastapi import APIRouter, Depends, Request

from models.request.booking.booking_request import CustomerBookingRequest
from models.response.base_response import BaseResponse
from models.response.booking.booking_response import BookingResponse
from models.response.booking.booking_with_boat_response import BookingWithBoatResponse
from services.impl.booking_service import BookingService
from services.meta.booking_service_meta import BookingServiceMeta
from utils.format_response import success_response
from utils.security.auth_checker import AuthChecker

router = APIRouter()


@router.get(
    "/list",
    response_model=BaseResponse[list[BookingWithBoatResponse]],
    summary="Mostra la lista di tutte le prenotazioni effettuate",
    description="Recupera e restituisce un elenco di tutte le prenotazioni registrate nel sistema."
)
async def booking_list(request: Request, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[list[BookingWithBoatResponse]]:
    return success_response(booking_service.find_all())

@router.post(
    "/make_reservation",
    response_model=BaseResponse[BookingResponse],
    summary="Questo endpoint permette di creare una nuova prenotazione nel sistema.",
    description="Accetta i dati della prenotazione e registra una nuova prenotazione nel sistema. Restituisce i dettagli della prenotazione creata con relativo ID di conferma."
)
async def make_reservation(request: Request, reservation_data: CustomerBookingRequest, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[BookingResponse]:
    logged_user = AuthChecker.get_logged_in_user(request)
    return success_response( booking_service.make_reservation(reservation_data, logged_user))