from django.contrib import messages


class PaymentError(Exception):
    pass


class UnableToTakePayment(PaymentError):

    pass
