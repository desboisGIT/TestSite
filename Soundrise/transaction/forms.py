from django import forms
from .models import CompteBancaire, PayPalAccount

class PayPalAccountForm(forms.ModelForm):
    class Meta:
        model = PayPalAccount
        fields = [
            'paypal_email',
            'paypal_password_hash',  # Consider using a password widget that hides the input
        ]       

class CompteBancaireForm(forms.ModelForm):
    class Meta:
        model = CompteBancaire
        fields = [
            'cb_name',
            'cb_number',
            'cb_code',
            'cb_date',  
        ]

