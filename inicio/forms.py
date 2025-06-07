from django import forms
from .models import Estacion

class EstacionForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ['nombre', 'orden']
