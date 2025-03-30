from enum import Enum


class Messages(Enum):
    GENERIC_ERROR = "Si è verificato un errore imprevisto."
    GENERIC_DATABASE_ERROR = "Si è verificato un errore nel database."
    MISSING_AUTHENTICATION_HEADER = "Non hai l'autorizzazione per accedere a questa risorsa."
    INVALID_AUTH_TOKEN = "Il token di autenticazione fornito non è valido o è scaduto."
    INSUFFICIENT_ROLE_PERMISSIONS = "Non hai il permesso per accedere a questa risorsa."
    NOT_FOUND = "La risorsa richiesta non è stata trovata."
    START_DATE_GREATHER_OR_EQUAL_THAN = "La data di inizio è maggiore o uguale alla data di fine."
    START_DATE_LESS_THAN_CURRENT = "La data di inizio è precedente al momento attuale."
    START_DATE_NEEDS_BUFFER = "La prenotazione deve iniziare almeno 1 ora dopo l'orario attuale."
    MIN_DURATION_NOT_SATISFIED = "La prenotazione deve avere una durata minima di 1 ora."
    MINIMUM_SEAT_REQUEST = "Il numero minimo di posti richiesti è 1."
    BOAT_ALREADY_BOOKED = "L'imbarcazione non è disponibile in quanto risulta già prenotata. Non è possibile procedere con la prenotazione. Prova con un altra imbarcazione o periodo di prenotazione."
    DELETE_OPERATION_NOT_ALLOWED = "Non puoi eliminare una prenotazione di un altro utente."
    NO_BOOKINGS_DELETED = "Nessuna prenotazione è stata eliminata."
    BOOKING_TO_EDIT_NOT_FOUND = "La prenotazione che si sta tentando di modificare non è stata trovata."
    BOOKING_CUSTOMER_ONLY = "La prenotazione può essere effettuata solo dal cliente e non da altri utenti."
    BOOKING_MODIFICATION_NOT_ALLOWED = "Non è possibile modificare una prenotazione già iniziata o terminata."
    CUSTOMER_ALREADY_HAS_BOOKING = "Hai già una prenotazione attiva per lo stesso arco temporale. Non è possibile effettuare prenotazioni simultaneamente. Cambia le date e riprova."
    ATTEMPT_TO_EDIT_INCOMPATIBLE_STATE = "Solo le prenotazioni con stato CONFIRMED possono essere modificate."