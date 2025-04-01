from datetime import datetime

import pytz


class DateTimeProvider:
    @staticmethod
    def get_timestamp_utc_sql() -> str:
        """
            Metodo di utilità per l'inserimento di date con SQL Alchemy.
        """
        return datetime.now(pytz.utc).isoformat()

    @staticmethod
    def parse_to_timezone(utc_timestamp: datetime) -> datetime:
        """
            Converte un timestamp UTC in un formato timezone specifico, in questo caso Europe/Rome.
            In futuro potrà essere gestito dinamicamente in base alla scelta dell'utente.
        """
        return utc_timestamp.astimezone(pytz.timezone("Europe/Rome"))

    @staticmethod
    def parse_input_datetime_to_utc(dt: datetime, assume_local: bool = True) -> datetime:
        if dt.tzinfo is None:
            if assume_local:
                dt = pytz.timezone("Europe/Rome").localize(dt)
            else:
                dt = dt.replace(tzinfo=pytz.utc)
        elif dt.tzinfo != pytz.utc:
            dt = dt.astimezone(pytz.utc)
        return dt