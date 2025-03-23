from enum import Enum


class Messages(Enum):
    GENERIC_ERROR = "An unexpected error has occurred."
    GENERIC_DATABASE_ERROR = "A database error has occurred."
    MISSING_AUTHENTICATION_HEADER = "You do not have authorization to access this resource."
    INVALID_AUTH_TOKEN = "The provided authentication token is invalid or expired."
    INSUFFICIENT_ROLE_PERMISSIONS = "You do not have permission to access this resource."
    NOT_FOUND = "The requested resource was not found."
    START_DATE_GREATHER_OR_EQUAL_THAN = "The start date is greater or equal than the end datetime."
    START_DATE_LESS_THAN_CURRENT = "The start date is less than the current datetime."
    START_DATE_NEEDS_BUFFER = "The booking must start at least 1 hour after the current time."