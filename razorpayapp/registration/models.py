from django.db import models
from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
# from django_countries.fields import CountryFieldeld
from uuid import uuid4
from django.template.defaultfilters import truncatechars
from django.core.validators import RegexValidator

# Create your models here.
def generate_id():
    return uuid4().hex[:32]

class Account(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False,
                            null=False, validators=[RegexValidator(
                                        regex="^[a-zA-Z][a-zA-Z\s]*$",
                                        message="Name should contain only \
                                        characters from a-z or A-Z")])
    email = models.EmailField(_('Email'))
    phonenumber = models.CharField(_('Phone Number'), max_length=25,
                                   blank=False, null=False,
                                   validators=[RegexValidator(
                                   regex="^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$",
                                    message="Invalid Phonenumber"
                                   )])
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    address = models.TextField(_('Address'), max_length=500, blank=True,
                               null=True)
    pan = models.CharField(_('PAN'), max_length=15, blank=False, null=True,
                           validators=[RegexValidator(
                               regex="^[A-Z]{5}[0-9]{4}[A-Z]{1}$",
                               message="Invalid PAN Number"
                           )])
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, blank=False, null=False)
    razp_id = models.CharField(max_length=22, blank=True, null=True)
    txn_id = models.CharField(max_length=64, default=generate_id)

    def __str__(self):
        return "%s" % (str(self.id))

    @property
    def short_txn_id(self):
        return truncatechars(self.txn_id, 10)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

class RazorpayTransaction(models.Model):
    TRANSACTION_INITIATED, TRANSACTION_CAPTURED, TRANSACTION_AUTHORIZED = (
        "initiated", "captured", "authorized"
    )

    TRANSACTION_FAILED, AUTHENTICATION_FAILED = (
        "capfailed", "authfailed"
    )

    account_id = models.OneToOneField(
        Account, on_delete=models.SET_NULL, null=True,
        related_name='rzptn'
    )
    transaction_date = models.DateField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False,
                                 blank=True)
    currency_type = models.CharField(max_length=15, null=False, blank=False)

    status = models.CharField(max_length=50)

    razorpay_id = models.CharField(
        max_length=22, null=False, blank=False, db_index=True
    )

    error_code = models.CharField(max_length=255, null=True, blank=True)

    error_message = models.CharField(max_length=256, null=True, blank=True)
    transaction_id = models.CharField(
        max_length=64, db_index=True, unique=True, default=generate_id
    )

    class Meta:
        ordering = ('-transaction_date',)

    @property
    def is_successful(self):
        return self.status == self.TRANSACTION_CAPTURED

    @property
    def is_pending(self):
        return self.status == self.TRANSACTION_AUTHORIZED

    @property
    def is_failed(self):
        return self.status not in (
            self.TRANSACTION_CAPTURED,
            self.TRANSACTION_AUTHORIZED,
            self.TRANSACTION_INITIATED
        )

    def __str__(self):
        return 'Razorpay Payment id is : %s' % self.razorpay_id
