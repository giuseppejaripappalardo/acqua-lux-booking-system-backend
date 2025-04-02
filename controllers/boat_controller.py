from fastapi import APIRouter, Depends, Request

from models.request.booking.search_boat_request import SearchBoatRequest, EditSearchBoatRequest
from models.response.base_response import BaseResponse
from models.response.boat.boat_response import BoatResponse
from services.impl.boat_service import BoatService
from services.meta.boat_service_meta import BoatServiceMeta
from utils.format_response import success_response

router = APIRouter()

@router.get(
    "/list",
    response_model=BaseResponse[list[BoatResponse]],
    summary="Mostra la lista di tutte imbarcazioni censite",
    description="Recupera e restituisce un elenco di tutte le imbarcazioni registrate nel sistema."
)
async def boats_list(request: Request, boat_service: BoatServiceMeta = Depends(BoatService)) -> BaseResponse[list[BoatResponse]]:
    return success_response(boat_service.find_all())

@router.post(
    "/search-available-boats",
    response_model=BaseResponse[list[BoatResponse]],
    summary="Mostra la lista delle imbarcazioni prenotabili nel range temporale fornito in input.",
    description="Recupera e restituisce un elenco di imbarcazioni disponibili alla prenotazione nel periodo specificato."
)
async def search_for_available_boats(reservation_data: SearchBoatRequest, boat_service: BoatServiceMeta = Depends(BoatService)) -> BaseResponse[list[BoatResponse]]:
    return success_response( boat_service.find_available_boats_for_booking(reservation_data, None))

@router.post(
    "/edit-search-available-boats",
    response_model=BaseResponse[list[BoatResponse]],
    summary="Mostra la lista delle imbarcazioni prenotabili nel range temporale fornito in input considerando la prenotazione da modificare.",
    description="Recupera e restituisce un elenco di imbarcazioni disponibili alla prenotazione nel periodo specificato considerando però l'imbarcazione prevista nella prenotazione da modificare."
)
async def edit_search_for_available_boats(reservation_data: EditSearchBoatRequest, boat_service: BoatServiceMeta = Depends(BoatService)) -> BaseResponse[list[BoatResponse]]:
    return success_response( boat_service.find_available_boats_for_booking(reservation_data, reservation_data.booking_id))