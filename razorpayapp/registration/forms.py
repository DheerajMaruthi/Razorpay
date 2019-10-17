from django import forms
from django.apps import apps
from decimal import Decimal
from registration import razorpay
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
import re

Account = apps.get_model('registration', 'Account')

AMOUNT_CHOICES = (
    ('1000', ' ₹ 1000'),
    ('5000', ' ₹ 5000'),
)

AMOUNT_CHOICES_DATA = ['1000', '5000',]


class RegistrationForm(forms.ModelForm):
    amount_option = forms.ChoiceField(choices=AMOUNT_CHOICES,
                                      required=False,
                                      initial='Other Amount',
                                      widget=forms.RadioSelect)
    address = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 3}))
    agree = forms.BooleanField()
    other_amount = forms.CharField(label='Amount', required=False,
                                   widget=forms.TextInput(
        attrs={'type': 'number', 'min': "100", 'pattern': '[0-9]+'}))

    def clean(self):
        amount_option_data = self.cleaned_data.get('amount_option')
        other_amount_data = self.cleaned_data.get('other_amount')
        my_dict = {}
        try:
            if amount_option_data == 'Other Amount':
                other_amount_data = Decimal(
                    self.cleaned_data.get('other_amount'))
        except Exception as e:
            my_dict['other_amount'] = "Invalid Amount"
            raise forms.ValidationError(my_dict)

        if amount_option_data in AMOUNT_CHOICES_DATA and other_amount_data:
            if amount_option_data == 'Other Amount' and other_amount_data < 100:
                my_dict['other_amount'] = "Please enter an amount greater \
                                           than ₹ 100"
                raise forms.ValidationError(my_dict)

    def save(self, commit=True, *args, **kwargs):
        data = super(RegistrationForm, self).save(commit=False, **kwargs)
        amount_option_data = self.cleaned_data.get('amount_option')
        if amount_option_data == 'Other Amount':
            data.amount = Decimal(self.cleaned_data.get('other_amount'))
        else:
            data.amount = Decimal(amount_option_data)
        data.payment_status = 'Not Initiated'
        data.save()
        account_model_instance = get_object_or_404(Account, pk=data.id)
        transaction_id = razorpay.start_transaction(account_model_instance,
                                                    data.amount, data.email)
        data.txn_id = transaction_id.transaction_id
        data.payment_status = "Initiated"
        data.save()
        return data

    class Meta:
        model = Account
        fields = ('amount_option', 'other_amount', 'name',
                  'email', 'phonenumber', 'address', 'agree')
