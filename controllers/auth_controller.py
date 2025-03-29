from fastapi import APIRouter, Depends, Response, Request

from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse
from models.response.base_response import BaseResponse
from services.impl.auth_service import AuthService
from services.meta.auth_service_meta import AuthServiceMeta
from utils.format_response import success_response

router = APIRouter()

@router.post(
    "/login",
    response_model=BaseResponse[TokenResponse],
    summary="Questo endpoint permette di creare un nuovo utente nel sistema.",
    description="Fornisce la possibilità di aggiungere un nuovo utente fornendo i dati necessari.")
async def login(response: Response, credentials: LoginRequest, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.login(response, credentials))

@router.post(
    "/get_token",
    response_model=BaseResponse[TokenResponse],
    summary="Il metodo serve per ottenere il token a partire da un cookie sicuro e non accessibile al frontend..",
    description="Utilizziamo il cookie come strumento di salvataggio del token. Questo ci garantisce maggiore robustezza in quanto un cookie http only e Secure previene problemi di attacchi XSS, tipici nel caso in cui si salva il token in un cookie non sicuro o in localStorage.")
async def get_token(request: Request, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.refresh(request))


@router.post(
    "/logout",
    response_model=BaseResponse,
    summary="Il metodo distrugge semplicemente il cookie.",
    description="Il metodo distrugge il cookie che contiene il token jwt. In un sistema più articolato avremmo previsto anche una blacklist. Ma va fuori dagli scopi del project work e quindi teniamo questo approccio semplificato.")
async def logout(request: Request, response: Response, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.logout(request, response))