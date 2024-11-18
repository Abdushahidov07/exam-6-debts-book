from django import forms
from .models import *

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['borrower', 'amount', 'interest_rate', 'due_date']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']