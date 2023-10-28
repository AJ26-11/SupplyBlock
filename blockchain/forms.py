from django import forms
from .models import SupplyChainData


class SupplyChainDataForm(forms.ModelForm):
    class Meta:
        model = SupplyChainData
        fields = ['data']
