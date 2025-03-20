import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from controllers.base_controller import BaseController
from routes.users import router as users_router

app = FastAPI()

"""
    Esponiamo le routes dei controller previsti
    dal project work.
"""
app.include_router(users_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
        Sovrascrivo la gestione della validazione pydantic per usare
        quella custom definita all'interno decorator del progetto, cosi
        da rendere i messaggi più parlanti e usare una interfaccia di risposta
        standard.
    """
    validation_errors = []
    for error in exc.errors():
        # Raccogli informazioni sull'errore
        loc = error.get('loc', [])
        field = loc[-1] if loc else 'unknown'
        msg = error.get('msg', 'Errore di validazione')

        validation_errors.append({
            "field": field,
            "details": msg
        })

    base_controller = BaseController()
    return base_controller.send_error(
        message="Data validation error",
        status_code=422,
        errors=validation_errors
    )
