from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User



class Carpeta(models.Model):
    nombre = models.CharField(max_length=256)
    fecha_creacion = models.DateTimeField(null=False)
    ultima_modificacion = models.DateTimeField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class Aplicacion(models.Model):
    nombre = models.CharField(max_length=256)
    descripcion = models.CharField(max_length = 5000)



class Analisis(models.Model):
    fecha = models.DateTimeField(null=False)
    informe = models.FileField() #upload_to media?
    carpeta =  models.ForeignKey(Carpeta, on_delete=models.DO_NOTHING) 
    aplicacion = models.ForeignKey(Aplicacion, on_delete=models.DO_NOTHING)


class Archivo(models.Model):
    nombre = models.CharField(max_length=256)
    fecha_creacion =  models.DateTimeField(blank=True, default=datetime.now) 
    arch = models.FileField()
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE)  #ver si esto esta bien.

class Resultado(models.Model): #esto lo estamos conciderando como una linea del resultado
    texto = models.CharField(max_length = 5000)
    detectado = models.FileField() #esto seria un json muy corto o un string (varia segun la aplicación que lo generó)
    archivo_origen = models.ForeignKey(Archivo, on_delete=models.DO_NOTHING) 
    numero_linea = models.IntegerField() 
    analisis = models.ForeignKey(Analisis, on_delete = models.CASCADE)


class Modelo(models.Model):
    nombre = models.CharField(max_length=256)
    descripcion = models.CharField(max_length = 5000)
    aplicacion = models.ForeignKey(Aplicacion, on_delete = models.DO_NOTHING)
    # modelo_entrenado