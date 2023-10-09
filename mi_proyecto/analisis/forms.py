from django import forms
from django.forms import DateField, ModelForm, ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from django.core.validators import validate_email 
from django.contrib.auth.models import User
import magic
from .models import Analisis, Carpeta, Colores, Preferencias, Modelo, Archivo
from mi_proyecto import settings


class FileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           help_text='</br> <br/> Seleccionar archivos .txt .docx .xlsx')
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            print(file.name.split('.'))
            #if file.name.split('.')[1] not in settings.TASK_UPLOAD_FILE_TYPES:
            if file.name.split('.')[1] not in ["txt", "docx" , "xlsx"]: 
                raise forms.ValidationError('File type is not supported')
        return file


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
                            widget=forms.Select(attrs={'class': 'form-control'},
                                                choices=Colores.choices))


class ResultadoViewForm(forms.Form):
    file_choice = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        analisis_id = kwargs.pop('analisis_id')
        super(ResultadoViewForm, self).__init__(*args, **kwargs)
        analisis = Analisis.objects.get(id=analisis_id)
        archivos = Archivo.objects.filter(carpeta=analisis.carpeta)
        file_choices = [(archivo.id, archivo.nombre) for archivo in archivos]
        file_choices.insert(0, ('all', 'Todos los archivos'))
        self.fields['file_choice'].choices = file_choices
        self.fields['file_choice'].label = 'Mostrar archivo'

