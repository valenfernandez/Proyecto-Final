from django.contrib import admin
from .models import Carpeta, Aplicacion, Analisis, Archivo, Resultado, Modelo

# Register your models here.
admin.site.register(Carpeta)
admin.site.register(Aplicacion)
admin.site.register(Analisis)
admin.site.register(Archivo)
admin.site.register(Resultado)
admin.site.register(Modelo)