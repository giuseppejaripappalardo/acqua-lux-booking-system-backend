from enum import Enum


class Messages(Enum):
    GENERIC_ERROR = "Si è verificato un errore imprevisto."
    GENERIC_DATABASE_ERROR = "Si è verificato un errore durante l'accesso al database."
    MISSING_AUTHENTICATION_HEADER = "Non sei autorizzato ad accedere a questa risorsa."
    INVALID_AUTH_TOKEN = "Il token di autenticazione fornito non è valido o è scaduto."
    INSUFFICIENT_ROLE_PERMISSIONS = "Non hai le autorizzazioni necessarie per accedere a questa risorsa."
    NOT_FOUND = "La risorsa richiesta non è stata trovata."
    START_DATE_GREATHER_OR_EQUAL_THAN = "La data di inizio non può essere successiva o uguale alla data di fine."
    START_DATE_LESS_THAN_CURRENT = "La data di inizio non può essere anteriore al momento attuale."
    START_DATE_NEEDS_BUFFER = "La prenotazione deve iniziare almeno un'ora dopo l'orario attuale."
    MIN_DURATION_NOT_SATISFIED = "La prenotazione deve avere una durata minima di un'ora."
    MINIMUM_SEAT_REQUEST = "Il numero minimo di posti prenotabili è uno."
    BOAT_ALREADY_BOOKED = "L'imbarcazione è già prenotata per il periodo selezionato. Non è possibile procedere con la prenotazione. Prova ad effettuare un'altra scelta."
    DELETE_OPERATION_NOT_ALLOWED = "Non puoi eliminare una prenotazione effettuata da un altro utente."
    NO_BOOKINGS_DELETED = "Non è stata eliminata alcuna prenotazione."
    BOOKING_TO_EDIT_NOT_FOUND = "La prenotazione che si sta cercando di modificare non è stata trovata."
    BOOKING_EDIT_INCOMPATIBLE_STATE = "La prenotazione è in uno stato che non consente la visualizzazione e/o modifica."
    BOOKING_CUSTOMER_ONLY = "Puoi modificare solo le prenotazione a te associate."
    GET_BOOKING_CUSTOMER_ONLY = "Puoi visualizzare solo le prenotazioni a te associate."
    BOOKING_MODIFICATION_NOT_ALLOWED = "Non è possibile modificare una prenotazione già iniziata o terminata."
    CUSTOMER_ALREADY_HAS_BOOKING = "Hai già una prenotazione attiva per lo stesso periodo. Non è possibile effettuare prenotazioni sovrapposte. Modifica le date e riprova."