from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from controllers import router as application_router
from exceptions.auth.auth_exception import AuthException
from exceptions.auth.role_exception import RoleException
from exceptions.generic.generic_database_exceptionen import GenericDatabaseException
from exceptions.generic.integrity_database_exception import IntegrityDatabaseException
from utils.logger_service import LoggerService
from utils.messages import Messages

app = FastAPI()

"""
    Esponiamo le controllers dei controller previsti
    dal project work.
"""
app.include_router(application_router)
logger_service = LoggerService().logger


@app.exception_handler(GenericDatabaseException)
@app.exception_handler(IntegrityDatabaseException)
async def database_exception_handler(request: Request, exc):
    """Gestore unificato per le eccezioni del database"""
    exc_type = exc.__class__.__name__

    # Loggo eventuali errori, in modo tale da poter recuperare
    # Sempre il dettaglio di ciò che si verifica.
    logger_service.error(f"{exc_type}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message if hasattr(exc, "message") else str(exc),
        }
    )

@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    """
        Questa eccezione viene sollevata in caso di problemi in fase di autenticazione.
        Ad esempio quando l'utente digita le credenziali errate.
    """

    # Loggo eventuali errori, in modo tale da poter recuperare
    # Sempre il dettaglio di ciò che si verifica.
    logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "message": str(exc),
        }
    )

@app.exception_handler(RoleException)
async def role_exception_handler(request: Request, exc: AuthException):
    """
        Questa eccezione viene sollevata in caso di ruolo non sufficiente per accedere ad una risorsa specifica.
    """

    # Loggo eventuali errori, in modo tale da poter recuperare
    # Sempre il dettaglio di ciò che si verifica.
    logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "message": str(exc),
        }
    )



@app.exception_handler(ValidationError)
async def pydantic_validation_error_handler(request: Request, exc: ValidationError):
    """Gestore per ValidationError di Pydantic, che si verifica durante la validazione di dati interni 
    al modello o dei dati già deserializzati, a differenza di RequestValidationError che viene sollevato 
    durante la validazione di input di una richiesta HTTP."""

    logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": str(exc),
        }
    )



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
        Questi tipi di errori vengono lanciati da pydantic nel caso in cui
        una richiesta non abbia i parametri corretti.
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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # Loggo eventuali errori, in modo tale da poter recuperare
        # Sempre il dettaglio di ciò che si verifica.
        logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Page not found",
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
        Gestore generico per le eccezioni
        Lo scopo è catturare tutti i tipi di eccezioni
        che di fatto non sono specifiche e quindi gestiste da un handler.
    """

    # Loggo eventuali errori, in modo tale da poter recuperare
    # Sempre il dettaglio di ciò che si verifica.
    logger_service.error(f"{exc.__class__.__name__}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": Messages.GENERIC_ERROR.value
        },
    )
