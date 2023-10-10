from django import forms
from .models import WalletInfo

class WalletForm(forms.ModelForm):
    class Meta:
        model = WalletInfo
        fields = '__all__'
