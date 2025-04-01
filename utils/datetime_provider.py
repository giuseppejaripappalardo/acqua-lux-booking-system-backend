from datetime import datetime, timezone

import pytz


class DateTimeProvider:
    @staticmethod
    def parse_input_datetime_to_utc(dt: datetime, assume_local: bool = False) -> datetime:
        if dt is None:
            raise ValueError("La data non può essere None.")

        if dt.tzinfo is None:
            if assume_local:
                dt = pytz.timezone("Europe/Rome").localize(dt)
            else:
                dt = dt.replace(tzinfo=pytz.utc)
        elif dt.tzinfo != pytz.utc:
            dt = dt.astimezone(pytz.utc)
        return dt