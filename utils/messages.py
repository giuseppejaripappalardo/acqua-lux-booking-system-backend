from enum import Enum


class Messages(Enum):
    GENERIC_ERROR = "An unexpected error has occurred."
    GENERIC_DATABASE_ERROR = "A database error has occurred."
    MISSING_AUTHENTICATION_HEADER = "You do not have authorization to access this resource."
    INVALID_AUTH_TOKEN = "The provided authentication token is invalid or expired."
    INSUFFICIENT_ROLE_PERMISSIONS = "You do not have permission to access this resource."
    NOT_FOUND = "The requested resource was not found."
