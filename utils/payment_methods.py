from enum import Enum


class PaymentMethods(Enum):
    BANK_TRANSFER = "BANK_TRANSFER"
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"