from fastapi import APIRouter, Depends, Request

from models.response.base_response import BaseResponse
from models.response.booking.booking_response import BookingResponse
from services.impl.booking_service import BookingService
from services.meta.booking_service_meta import BookingServiceMeta
from utils.format_response import success_response

router = APIRouter()


@router.get(
    "/list",
    response_model=BaseResponse[list[BookingResponse]],
    summary="Mostra la lista di tutte le prenotazioni effettuate",
    description="Recupera e restituisce un elenco di tutte le prenotazioni registrate nel sistema."
)
async def booking_list(request: Request, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[list[BookingResponse]]:
    return success_response(booking_service.find_all())