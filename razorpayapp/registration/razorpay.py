from uuid import uuid4
import razorpay
from .models import Account, RazorpayTransaction as IntialTransaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings

rz_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
)


def start_transaction(account_id, amount, email=None):
    try:
        currency = 'INR'
        intial_transaction = IntialTransaction(
            account_id=account_id, amount=amount, currency_type=currency,
            status="initiated", transaction_id=uuid4().hex[:32], email=email
        )
        intial_transaction.save()
        return intial_transaction
    except Exception as e:
        print(str(e))


def update_transaction_details(razorpay_id, transaction_id):
    try:
        payment = rz_client.payment.fetch(razorpay_id)
    except Exception as e:
        print("Clinet not found for the transaction")
    try:
        transaction_details = IntialTransaction.objects.get(
            transaction_id=transaction_id)
    except Exception as e:
        print("Transaction failed update")
    if(int(transaction_details.amount * 100) != payment['amount']
       or transaction_details.currency_type != payment['currency']
       or transaction_id != transaction_details.transaction_id):
        raise Exception
    transaction_details.status = payment["status"]
    transaction_details.razorpay_id = razorpay_id
    transaction_details.save()
    return transaction_details


def capture_transaction(request, rz_id):
    """
    capture the payment
    """
    try:
        txn = IntialTransaction.objects.get(razorpay_id=rz_id)
        rz_client.payment.capture(rz_id, int(txn.amount * 100))
        txn.status = "captured"
        txn.save()
    except Exception as e:
        messages.error(request, str(e))
        raise ValueError('A very specific bad thing happened.')
    return txn


def initiate_bank_transfer(request, rz_id):
    try:
        payment_details = rz_client.payment.fetch(rz_id)
        amount = payment_details.get('amount')
        fee = payment_details.get('fee')
        currency_type = payment_details.get('currency')
        transfer_amount = amount - fee
        transfer_commision = (transfer_amount/100) * (0.25/100) * (1.18)
        transfer_commision = int(transfer_commision * 100)
        transfer_amount = transfer_amount - transfer_commision
        rz_client.payment.transfer(rz_id, {'transfers': [{
                                            'account': 'acc_CHxDVE8ZxE101A',
                                            'amount': transfer_amount,
                                            'currency': currency_type}]})
    except Exception as e:
        print(f"The exception occured is {str(e)}")
