import os
from datetime import datetime, timedelta

import pytz
from fastapi import Depends, Response, Request

from database.entities.user import User
from database.repositories.impl.user_repository import UserRepository
from exceptions.auth.auth_exception import AuthException
from models.object.token_payload import TokenPayload
from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse
from models.response.user.user_response import UserResponse
from services.meta.auth_service_meta import AuthServiceMeta
from utils.enum.messages import Messages
from utils.logger_service import LoggerService
from utils.security.bcrypt_hash_password import PassowrdHasher
from utils.security.jwt_utils import JwtUtils


class AuthService(AuthServiceMeta):
    _logger_service = None
    _user_repository = None
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", None)
    JWT_COOKIE_NAME = "jwt_token"

    def __init__(self, logger_service: LoggerService = Depends(LoggerService),
                 user_repository: UserRepository = Depends(UserRepository)):
        self._logger_service = logger_service
        self._user_repository = user_repository

    def login(self, response: Response, login: LoginRequest) -> TokenResponse:
        user: User = self._user_repository.get_by_username(login.username)

        if user is None or PassowrdHasher().bscript_verify_password(login.password, user.password) is False:
            self._logger_service.logger.error("Invalid username or password")
            raise AuthException("Invalid username or password")

        payload: TokenPayload = TokenPayload(
            sub=str(user.id),
            role=user.role.name.value,
            exp=datetime.now(pytz.utc) + timedelta(minutes=int(self.ACCESS_TOKEN_EXPIRE_MINUTES))
        )

        response_jwt_token = JwtUtils.create_access_token(payload)

        """
            Per semplificare il processo, considerato anche che l'autenticazione è fuori dagli obiettivi del project work,
            utilizziamo un cookie sicuro per salvare il token JWT. Questo ci consente di evitare di utilizzare localStorage
            lato frontend, visto che è vulnerabile ad attacchi XSS. 
    
            Normalmente in un sistema in produzione si dovrebbe prevedere un refresh token anziché il token JWT nel cookie. 
            Se il frontend ha bisogno di ricevere nuovamente il token (magari perché lo utilizziamo in maniera volatile 
            senza persisterlo per ragioni di security), normalmente si può mandare la richiesta, il backend controlla 
            il refresh token nel cookie che sarà accessibile solo da quest'ultimo e risponde con il token jwt.
    
            Poi ovviamente si dovrebbe prevedere una blacklist così da invalidare il token ed evitare che possa 
            essere usato in futuro.
        """
        response.set_cookie(
            key=self.JWT_COOKIE_NAME,
            value=response_jwt_token,
            httponly=True,
            secure=True,
            samesite="lax",
            expires=int(self.ACCESS_TOKEN_EXPIRE_MINUTES) * 60
        )

        logged_user_response = UserResponse.model_validate(user)

        return TokenResponse(
            jwt_token=response_jwt_token,
            user=logged_user_response
        )

    def refresh(self, request: Request) -> TokenResponse:
        cookie_value = request.cookies.get(self.JWT_COOKIE_NAME)
        if cookie_value is None:
            raise AuthException(message=Messages.MISSING_AUTHENTICATION_HEADER.value)

        """
            Inserito qui il decode poiché al suo interno verifica anche la validità del token salvato nei cookie.   
            Se non è valido fa il raise di un eccezione  
        """
        token_payload: TokenPayload = JwtUtils.decode_token(cookie_value)

        user: User = self._user_repository.get_by_id(int(token_payload.sub))
        self._logger_service.logger.info(f"User: {user.username} retrieving token")

        return TokenResponse(
            jwt_token=cookie_value,
            user=UserResponse.model_validate(user)
        )

    def logout(self, request: Request, response: Response) -> None:
        cookie_value = request.cookies.get(self.JWT_COOKIE_NAME)
        """
            Se il cookie non esiste siamo apposto.
        """
        if cookie_value is None:
            pass
        response.delete_cookie(key=self.JWT_COOKIE_NAME)