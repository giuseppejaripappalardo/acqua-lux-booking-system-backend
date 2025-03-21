import functools
import traceback

from pydantic import ValidationError

from exceptions.auth.auth_exception import AuthException
from exceptions.generic.generic_database_exceptionen import GenericDatabaseException
from exceptions.generic.integrity_database_exception import IntegrityDatabaseException
from messages import Messages


def handle_exceptions(func):
    """
        Ho creato questo decoratore perchè mi sembrava poco elengate
        dover ripetere la catena degli except in ogni controller.
        In questo modo sfruttando il decorator posso annotare i metodi
        dei controller e avere una gestione degli errori centralizzata.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except GenericDatabaseException as e:
            _log_error(self, func.__name__, e, "GenericDatabaseException")
            return self.send_error(e.message)
        except IntegrityDatabaseException as e:
            _log_error(self, func.__name__, e, "IntegrityDatabaseException")
            return self.send_error(e.message)
        except ValidationError as e:
            _log_error(self, func.__name__, e, "ValidationError")
            return self.send_error(str(e), status_code=422)
        except AuthException as e:
            _log_error(self, func.__name__, e, "AuthException")
            return self.send_error(str(e), status_code=e.code)
        except Exception as e:
            _log_error(self, func.__name__, e, "Exception")
            return self.send_error(Messages.GENERIC_ERROR.value)

    def _log_error(self_obj, func_name, exception, exception_type):
        if hasattr(self_obj, '_logger_service'):
            trace_str = traceback.format_exc()
            error_msg = f"[{exception_type}] in {func_name}: {str(exception)}"
            if hasattr(exception, 'message'):
                error_msg = f"[{exception_type}] in {func_name}: {exception.message}"
            self_obj._logger_service.logger.error(error_msg)
            self_obj._logger_service.logger.error(f"Traceback:\n{trace_str}")

    return wrapper
