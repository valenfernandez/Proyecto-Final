from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Carpeta, Archivo, Analisis, Aplicacion, Resultado, Modelo, Preferencias, Grafico, Grafico_Imagen, Tabla
from .forms import AnalisisForm, PreferenciasForm, CarpetaForm, FileForm
from .nlp import procesar_analisis

# Create your views here.

@login_required
def home(request): 
    response = redirect('/principal')
    return response

@login_required
def principal(request):
    return render(request, "analisis/principal.html") 

@login_required
def config(request):
    user = request.user

    try:
        preferencias = Preferencias.objects.get(usuario = user)
    except Preferencias.DoesNotExist:
        preferencias = Preferencias(usuario = user, color = 'CLASICO')
    form_preferencias = PreferenciasForm(request.POST or None, request.FILES or None, instance=preferencias)
     
    context = {
        "usuario": user,
        "color_actual" : preferencias.color,
        "form_preferencias" : form_preferencias,
    }

    if form_preferencias.is_valid():
        form_preferencias.save()
        response = redirect('/config')
        return response

    return render(request, "analisis/config.html", context=context) 

@login_required
def carpetas(request):
    usuario_actual = request.user
    context = {
        "carpetas": Carpeta.objects.filter(usuario = usuario_actual),
    }
    return render(request, "analisis/carpetas.html", context= context) 

@login_required
def carpeta(request, id_carpeta):

    usuario_actual = request.user
    carpeta = Carpeta.objects.get(id = id_carpeta)

    if carpeta.usuario != usuario_actual:
        return HttpResponse("No tiene permiso para ver esta carpeta")

    form_file = FileForm(request.POST or None, request.FILES or None)
    context = {
        "carpeta": carpeta,
        "archivos": Archivo.objects.filter(carpeta = carpeta),
        "form_file" : form_file,
    }
    if form_file.is_valid():
        for f in request.FILES.getlist('file'):
            nombre = f.name
            archivo = Archivo(nombre =nombre, arch = f, carpeta = carpeta, fecha_creacion = datetime.now())
            archivo.save()
        response = redirect('/carpeta/'+str(carpeta.id))
        return response
    return render(request, "analisis/carpeta.html", context=context) 

@login_required
def aplicacion(request, id_app):

    analisis = Analisis(informe ='')

    aplicacion = Aplicacion.objects.get(id = id_app)
    form_analisis = AnalisisForm(request.POST or None, request.FILES or None, instance=analisis, aplicacion = aplicacion)
    
    context = {
        "aplicacion": aplicacion,
        "form_analisis" : form_analisis,
    }

    if form_analisis.is_valid():
        form_analisis.save()

        procesar_analisis(analisis, request.user)
        
        response = redirect('/resultado/'+str(analisis.id))
        return response
    return render(request, "analisis/aplicacion.html", context=context) 

@login_required
def resultados(request):
    carpetas = Carpeta.objects.filter(usuario = request.user)
    context = {
        'analisis' : Analisis.objects.filter(carpeta__in = carpetas).order_by("-id")
    }
    return render(request, "analisis/resultados.html",context=context) 


@login_required
def resultado(request, id_analisis):
    """
    TODO: Agrupar los resultados por archivo de origen y mostrarlos separados 
    (podria ser separados por tabs o algo asi, o en distintas secciones)
    
    """
    usuario_actual = request.user
    carpetas = Carpeta.objects.filter(usuario = request.user)
    analisis = Analisis.objects.get(id = id_analisis)
    if analisis.carpeta.usuario != usuario_actual:
        return HttpResponse("No tiene permiso para ver este resultado")
    
    tablas = Tabla.objects.filter(analisis = analisis)
    graficos = Grafico.objects.filter(analisis = analisis)
    imagenes = Grafico_Imagen.objects.filter(analisis = analisis)
    resultados = Resultado.objects.filter(analisis = analisis)
    

    if analisis.modelo.nombre == 'entidades':

        context = {
        'analisis' : analisis,
        'aplicacion' : analisis.modelo.aplicacion,
        'resultados' : resultados,
        'wordclouds' : imagenes,
        'graficos' : graficos,
        'tabla_distribucion' : Tabla.objects.get(analisis = analisis, nombre = 'Distribucion de entidades'),
        'tabla_rep': Tabla.objects.get(analisis = analisis, nombre = 'Entidades que se repiten'),
        'grafico_distribucion' : Grafico.objects.get(analisis = analisis, nombre = 'Distribucion de entidades'),
        'grafico_ents_archivo' : Grafico.objects.get(analisis = analisis, nombre = 'Entidades por archivo'),
        'grafico_comp_archivos' : Grafico.objects.get(analisis = analisis, nombre = 'Composicion de entidades por archivo'),
        'grafico_lineas_ents': Grafico.objects.get(analisis = analisis, nombre = 'Relacion entre numero de linea y entidades'),
        }
        
        return render(request, "analisis/resultado_entidades.html", context= context)
    
    elif analisis.modelo.nombre == 'clasificador':
        context = {
        'analisis' : analisis,
        'aplicacion' : analisis.modelo.aplicacion,
        'resultados' : resultados,
        'imagenes' : imagenes,
        'graficos' : graficos,
        'tablas' : tablas,
        }
        
        return render(request, "analisis/resultado_clasificador.html", context= context)
    else:
        context = {
        'analisis' : Analisis.objects.filter(carpeta__in = carpetas).order_by("-id")
        }
        return render(request, "analisis/resultados.html", context= context) 




@login_required
def nueva_carpeta(request):
    carpeta = Carpeta(usuario = request.user, fecha_creacion=datetime.now(), ultima_modificacion=datetime.now(), nombre = '')
    form_carpeta = CarpetaForm(request.POST or None, request.FILES or None, instance=carpeta)
    context = {
        'form_carpeta' : form_carpeta,
    }
    if form_carpeta.is_valid():
        form_carpeta.save()
        response = redirect('/carpetas')
        return response
    return render(request, "analisis/nueva_carpeta.html", context = context) 


@login_required
def borrar_archivo(request, id_archivo):
    archivo = Archivo.objects.get(id = id_archivo)
    carpeta = archivo.carpeta
    usuario_actual = request.user
    if carpeta.usuario != usuario_actual:
        return HttpResponse("No tiene permiso para borrar este archivo")
    archivo.delete()
    response = redirect('/carpeta/'+str(carpeta.id))
    return response


@login_required
def borrar_resultado(request, id_analisis):
    #TODO
    analisis = Analisis.objects.get(id = id_analisis)
    usuario_actual = request.user
    if analisis.carpeta.usuario != usuario_actual:
        return HttpResponse("No tiene permiso para borrar este resultado")
    return 1


"""
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

class CarpetaDeleteView(DeleteView):
    model = Carpeta
    success_url = reverse_lazy('carpeta-list')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.warning(request, f"Deleting {obj.nombre} will also delete all associated files. Please download the results before deleting if possible.")
        return super().post(request, *args, **kwargs)
    
"""