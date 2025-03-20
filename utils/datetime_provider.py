from datetime import datetime
import pytz
from sqlalchemy import text, TextClause


class DateTimeProvider:
    @staticmethod
    def get_timestamp_utc_sql() -> TextClause:
        """
            Metodo di utilità per l'inserimento di date con SQL Alchemy.
        """
        return text("CURRENT_TIMESTAMP")

    @staticmethod
    def parse_to_timezone(utc_timestamp: datetime) -> datetime:
        """
            Converte un timestamp UTC in un formato timezone specifico, in questo caso Europe/Rome.
            In futuro potrà essere gestito dinamicamente in base alla scelta dell'utente.
        """
        return utc_timestamp.astimezone(pytz.timezone("Europe/Rome"))