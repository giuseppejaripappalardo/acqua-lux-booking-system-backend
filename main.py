from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from controllers.base_controller import BaseController
from routes import router as application_router
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

"""
    Esponiamo le routes dei controller previsti
    dal project work.
"""
app.include_router(application_router)




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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return BaseController().send_error(
            message="Page not found",
            status_code=404,
            errors=[{"details": "The requested page was not found."}]
        )

    return BaseController().send_error(
        message=exc.detail,
        status_code=exc.status_code,
        errors=None
    )