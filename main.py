from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from controllers import router as application_router
from exceptions.auth.auth_exception import AuthException
from exceptions.auth.role_exception import RoleException
from exceptions.booking.boat_already_booked_exception import BoatAlreadyBookedException
from exceptions.generic.generic_database_exception import GenericDatabaseException
from exceptions.generic.integrity_database_exception import IntegrityDatabaseException
from exceptions.users.user_already_exists import UserAlreadyExists
from models.object.token_payload import TokenPayload
from utils.security.auth_checker import AuthChecker
from utils.logger_service import LoggerService
from utils.enum.messages import Messages

app = FastAPI()

"""
    Esponiamo le controllers dei controller previsti
    dal project work.
"""
app.include_router(application_router)
logger_service = LoggerService().logger

"""
    Middleware per proteggere le routes.
    Verifichiamo se la routes richiede autenticazione
    e gestiamo la request di conseguenza
"""


@app.middleware("http")
async def check_auth_and_role(request: Request, call_next):
    public_routes: list[str] = [
        "/api/v1/auth/login",
        "/api/v1/auth/get_token",
        "/api/v1/docs",
        "/api/v1/redoc",
        "/api/v1/openapi.json",
    ]

    # Se l'url visitato è presente nella lista di quelli pubblici
    # Restituiamo la risposta senza effettuare il controllo per per l'autenticazione
    if request.url.path in public_routes:
        return await call_next(request)
    else:
        # In tutti gli altri casi chiamiamo il metodo per controllare se l'utente è autenticato ed infine ritorniamo la risposta.
        user: TokenPayload = AuthChecker.assert_user_is_authenticated(request)

    response = await call_next(request)
    return response


"""
    Gestione delle eccezioni generali.
"""


@app.exception_handler(AuthException)
@app.exception_handler(UserAlreadyExists)
@app.exception_handler(BoatAlreadyBookedException)
@app.exception_handler(GenericDatabaseException)
@app.exception_handler(IntegrityDatabaseException)
@app.exception_handler(RoleException)
@app.exception_handler(ValidationError)
@app.exception_handler(StarletteHTTPException)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc):
    """
        Gestore unificato per le eccezioni:
        Database
        Integrity
        Auth Exception
        Role Exception
        Validation Exception
    """
    exc_type = exc.__class__.__name__

    if hasattr(exc, "status_code") and exc.status_code == 404:
        # Loggo eventuali errori, in modo tale da poter recuperare
        # Sempre il dettaglio di ciò che si verifica.
        logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": Messages.NOT_FOUND.value,
            },
        )


    if hasattr(exc, "code") and isinstance(exc.code, int):
        exception_code = exc.code
    elif hasattr(exc, "status_code") and isinstance(exc.status_code, int):
        exception_code = exc.status_code
    else:
        exception_code = 500

    logger_service.error(f"{exc_type}: {str(exception_code)}")
    logger_service.error(f"{exc.message}")

    return JSONResponse(
        status_code=exception_code,
        content={
            "success": False,
            "message": exc.message if hasattr(exc, "message") else str(exc),
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
        Questi tipi di errori vengono lanciati da pydantic nel caso in cui
        una richiesta non abbia i parametri corretti.
        Gestiamo la risposta a queste eccezioni separatamente cosi da formattare meglio
        la risposta e fornire un feedback dettagliato su quale campo ha avuto un errore.
    """
    validation_errors = []
    for error in exc.errors():
        loc = error.get('loc', [])
        field = loc[-1] if loc else 'unknown'
        msg = error.get('msg', 'Errore di validazione')

        validation_errors.append({
            "field": field,
            "details": msg
        })

    # Loggo eventuali errori, in modo tale da poter recuperare
    # Sempre il dettaglio di ciò che si verifica.
    logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": validation_errors,
        },
    )


"""
    Gestione delle eccezioni generali.
"""
