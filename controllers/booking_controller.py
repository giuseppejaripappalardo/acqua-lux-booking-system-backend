from fastapi import APIRouter, Depends, Request

from models.object.token_payload import TokenPayload
from models.request.booking.booking_delete_request import BookingDeleteRequest
from models.request.booking.booking_request import CustomerBookingRequest, EditBookingRequest, GetBookingByIdRequest
from models.response.base_response import BaseResponse
from models.response.booking.booking_response import BookingResponse
from models.response.booking.booking_with_boat_response import BookingWithBoatResponse
from services.impl.booking_service import BookingService
from services.meta.booking_service_meta import BookingServiceMeta
from utils.format_response import success_response
from utils.logger_service import LoggerService
from utils.security.auth_checker import AuthChecker

router = APIRouter()


@router.get(
    "/list",
    response_model=BaseResponse[list[BookingWithBoatResponse]],
    summary="Mostra la lista di tutte le prenotazioni effettuate",
    description="Recupera e restituisce un elenco di tutte le prenotazioni registrate nel sistema.",
    responses={
        401: {
            "description": "Errore di autenticazione - Utente non autenticato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Invalid authentication token"}
                }
            }
        }
    }
)
async def booking_list(request: Request, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[list[BookingWithBoatResponse]]:
    logged_user: TokenPayload = AuthChecker.get_logged_in_user(request)
    return success_response(booking_service.find_all(logged_user))


@router.get(
    "/view",
    response_model=BaseResponse[BookingWithBoatResponse],
    summary="Restituisce i dettagli della prenotazione specificata.",
    description="Recupera e restituisce tramite id una prenotazione registrata a sistema.",
    responses={
        401: {
            "description": "Errore di autenticazione - Utente non autenticato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Invalid authentication token"}
                }
            }
        },
        403: {
            "description": "Errore di autorizzazione - Utente non autorizzato a visualizzare questa prenotazione",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Only the customer who made the booking can view it"}
                }
            }
        },
        404: {
            "description": "Errore - Prenotazione non trovata",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Not found"}
                }
            }
        },
        422: {
            "description": "Errore - Stato della prenotazione incompatibile",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Booking status is incompatible with this operation"}
                }
            }
        }
    }
)
async def view(request: Request, booking_id: int, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[BookingWithBoatResponse]:
    logger = LoggerService().logger
    logger.info(f"Request to view booking with id: {booking_id}")
    logged_user: TokenPayload = AuthChecker.get_logged_in_user(request)
    return success_response(booking_service.get_by_id(booking_id, logged_user))


@router.post(
    "/add",
    response_model=BaseResponse[BookingWithBoatResponse],
    summary="Questo endpoint permette di creare una nuova prenotazione nel sistema.",
    description="Accetta i dati della prenotazione e registra una nuova prenotazione nel sistema. Restituisce i dettagli della prenotazione creata con relativo ID di conferma.",
    responses={
        401: {
            "description": "Errore di autenticazione - Utente non autenticato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Invalid authentication token"}
                }
            }
        },
        409: {
            "description": "Errore - Imbarcazione già prenotata o cliente ha già una prenotazione per lo stesso periodo",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "The boat is already booked for the selected period"}
                }
            }
        },
        422: {
            "description": "Errore di validazione - Dati della prenotazione non validi",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Validation error"}
                }
            }
        }
    }
)
async def make_reservation(request: Request, reservation_data: CustomerBookingRequest, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[BookingWithBoatResponse]:
    logged_user = AuthChecker.get_logged_in_user(request)
    return success_response(booking_service.make_reservation(reservation_data, logged_user))


@router.post(
    "/edit",
    response_model=BaseResponse[BookingWithBoatResponse],
    summary="Questo endpoint permette di modificare una prenotazione nel sistema.",
    description="Questo endpoint consente di aggiornare i dettagli di una prenotazione esistente. Accetta i dati della prenotazione da modificare e li elabora, verificando che l'utente abbia le autorizzazioni necessarie. Restituisce i dettagli aggiornati della prenotazione con il relativo ID di conferma. La modifica è possibile solo se l'imbarcazione è disponibile per il nuovo periodo richiesto.",
    responses={
        401: {
            "description": "Errore di autenticazione - Utente non autenticato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Invalid authentication token"}
                }
            }
        },
        403: {
            "description": "Errore di autorizzazione - Utente non autorizzato a modificare questa prenotazione",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Only the customer who made the booking can edit it"}
                }
            }
        },
        404: {
            "description": "Errore - Prenotazione non trovata",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Booking to edit not found"}
                }
            }
        },
        409: {
            "description": "Errore - Imbarcazione già prenotata per il periodo selezionato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "The boat is already booked for the selected period"}
                }
            }
        },
        422: {
            "description": "Errore - Stato della prenotazione incompatibile o prenotazione già iniziata",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Booking modification is not allowed for bookings that have already started"}
                }
            }
        }
    }
)
async def edit_reservation(request: Request, edit_reservation_data: EditBookingRequest, booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[BookingWithBoatResponse]:
    logged_user = AuthChecker.get_logged_in_user(request)
    return success_response(booking_service.edit_reservation(edit_reservation_data, logged_user))

@router.post(
    "/delete",
    response_model=BaseResponse[BookingResponse],
    summary="Questo endpoint permette di modificare lo stato di una prenotazione esistente nel sistema in CANCELLED.",
    description="Setta lo stato di una prenotazione esistente in CANCELLED.",
    responses={
        401: {
            "description": "Errore di autenticazione - Utente non autenticato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Invalid authentication token"}
                }
            }
        },
        403: {
            "description": "Errore di autorizzazione - Utente non autorizzato a cancellare questa prenotazione",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Delete operation not allowed"}
                }
            }
        },
        404: {
            "description": "Errore - Prenotazione non trovata",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Not found"}
                }
            }
        },
        422: {
            "description": "Errore - Prenotazione già cancellata o prenotazione già iniziata",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Booking already deleted or booking has already started"}
                }
            }
        }
    }
)
async def delete_reservation(request: Request, booking_request: BookingDeleteRequest,booking_service: BookingServiceMeta = Depends(BookingService)) -> BaseResponse[BookingResponse]:
    logged_user = AuthChecker.get_logged_in_user(request)
    return success_response(booking_service.delete_booking(logged_user, booking_request.booking_id))
