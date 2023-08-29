from django import forms
from django.forms import DateField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from django.core.validators import validate_email 
from django.contrib.auth.models import User

from .models import Analisis, Carpeta, Colores, Preferencias, Modelo


class CarpetaForm(ModelForm):
    class Meta:
        model = Carpeta
        fields = ['nombre']
    nombre = forms.CharField(label='Nombre', 
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))


class AnalisisForm(ModelForm): 

    def __init__(self, *args, **kwargs):
        aplicacion = kwargs.pop('aplicacion')
        modelos = Modelo.objects.filter(aplicacion = aplicacion)
        super(AnalisisForm, self).__init__(*args, **kwargs)
        self.fields['modelo'] = forms.ModelChoiceField(
                required=True,
                queryset=modelos,
                widget=forms.Select(attrs={'class': 'form-control'}, choices = modelos), 
				label='Modelo')
        self.fields['carpeta'].help_text = '<br/> Se analizaran todos los achivos pertenecientes a la carpeta seleccionada.'


    class Meta:
        model = Analisis
        fields = ['carpeta', 'modelo']
        
    carpeta = forms.ModelChoiceField(
        queryset=Carpeta.objects.all(),
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class PreferenciasForm(ModelForm):
    class Meta:
        model = Preferencias
        fields = ['color']
    color = forms.CharField(label='Esquema de colores', 
                            widget=forms.Select(attrs={'class': 'form-control'},choices=Colores.choices))