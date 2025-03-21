from datetime import datetime

import pytz


class DateTimeProvider:
    @staticmethod
    def get_timestamp_utc_sql() -> str:
        """
            Metodo di utilità per l'inserimento di date con SQL Alchemy.
        """
        return datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f")

    @staticmethod
    def parse_to_timezone(utc_timestamp: datetime) -> datetime:
        """
            Converte un timestamp UTC in un formato timezone specifico, in questo caso Europe/Rome.
            In futuro potrà essere gestito dinamicamente in base alla scelta dell'utente.
        """
        return utc_timestamp.astimezone(pytz.timezone("Europe/Rome"))