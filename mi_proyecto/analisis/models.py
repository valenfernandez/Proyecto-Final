from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy


class Colores(models.TextChoices):
    CLASICO            = "CLASICO", gettext_lazy("Clasico")
    AR            = "AR", gettext_lazy("Azul a Rosa") #AZUL ROSA
    AM            = "AM", gettext_lazy("Azul a Amarillo") #AZUL AMARILLO

class Carpeta(models.Model):
    nombre = models.CharField(max_length=256)
    fecha_creacion = models.DateTimeField(null=False)
    ultima_modificacion = models.DateTimeField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return (
            f"{self.nombre}"
        )


class Aplicacion(models.Model):
    class Meta:
        verbose_name_plural = "Aplicaciones"
    nombre = models.CharField(max_length=256)
    descripcion = models.CharField(max_length = 5000)
    
    def __str__(self):
        return (
            f"{self.nombre}"
        )


class Modelo(models.Model):
    nombre = models.CharField(max_length=256)
    descripcion = models.CharField(max_length = 5000)
    aplicacion = models.ForeignKey(Aplicacion, on_delete = models.DO_NOTHING)
    def __str__(self):
        return (
            f"{self.nombre}"
        )
    

class Analisis(models.Model):
    class Meta:
        verbose_name_plural = "Analisis"
    fecha = models.DateTimeField(null=False, default=datetime.now)
    informe = models.TextField(blank=True, null=True) #capaz esto lo sacamos y en su ligar armamos el html del informe con los graficos y las imagenes. O aca se pone el template del informe
    carpeta =  models.ForeignKey(Carpeta, on_delete=models.CASCADE, blank=True)  # si se borra la carpeta se borra el analisis. Esto no deberia pasar pero da un error al borrar archivos si no esta esto. 
    modelo = models.ForeignKey(Modelo, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return (
            f"{self.fecha} - {self.carpeta}"
        )

class Archivo(models.Model):
    nombre = models.CharField(max_length=256)
    fecha_creacion =  models.DateTimeField(blank=True, default=datetime.now) 
    arch = models.FileField(upload_to='archivos/') #upload_to='archivos/'
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE)
    def __str__(self):
        return (
            f"{self.nombre}"
        )

class Resultado(models.Model): #esto lo estamos conciderando como una linea del resultado
    texto = models.CharField(max_length = 5000)
    detectado = models.TextField() #esto seria un json muy corto o un string (varia segun la aplicación que lo generó)
    archivo_origen = models.ForeignKey(Archivo, on_delete=models.CASCADE)  #SI SE BORRA EL ARCHIVO DE ORIGEN SE BORRA EL RESULTADO! (esto es para evitar errores de integridad)
    numero_linea = models.IntegerField() 
    analisis = models.ForeignKey(Analisis, on_delete = models.CASCADE)
    html = models.TextField(default=" ")
    def __str__(self):
        return (
            f"{self.analisis} - {self.numero_linea}"
        )
    


class Preferencias(models.Model):
    #tecnicamente aca podria existir la inconsistencia de que un usuario tenga mas de una preferencia
    #conceptualmente no se si esto es lo mejor pero es lo mas facil de implementar
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    color = models.CharField(
        max_length=10,
        choices=Colores.choices,
        default=Colores.CLASICO,
    )
    def __str__(self):
        return (
            f"{self.usuario} - {self.color}"
        )

class Grafico(models.Model):
    analisis = models.ForeignKey(Analisis, on_delete = models.CASCADE)
    nombre = models.CharField(max_length=256)
    chart = models.TextField(blank=True, null=True) #grafico de altair en formato json
    def __str__(self):
        return (
            f"{self.nombre}"
        )

class Grafico_Imagen(models.Model):
    analisis = models.ForeignKey(Analisis, on_delete = models.CASCADE)
    nombre = models.CharField(max_length=256)
    imagen = models.ImageField(upload_to='static/graficos/', blank=True, null=True) #imagen del grafico (wordcloud, etc)
    def __str__(self):
        return (
            f"{self.nombre}"
        )
    
class Tabla(models.Model):
    analisis = models.ForeignKey(Analisis, on_delete = models.CASCADE)
    nombre = models.CharField(max_length=256)
    tabla = models.TextField(blank=True, null=True) #tabla de pandas en formato html
    def __str__(self):
        return (
            f"{self.nombre}"
        )