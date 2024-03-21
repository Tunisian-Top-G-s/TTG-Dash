from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'pair', 'amount', 'img', 'status']
        widgets = {
            'type': forms.Select(choices=Transaction.TYPE, attrs={'class': 'form-control'}),
            'pair': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class OrderForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    address = forms.CharField(label="Address", max_length=200)
    city = forms.CharField(label="City", max_length=100)
    state = forms.CharField(label="State", max_length=100)
    zip_code = forms.CharField(label="Zip Code", max_length=10)