from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Carpeta, Archivo, Analisis, Aplicacion, Resultado, Modelo, Preferencias
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
    carpeta = Carpeta.objects.get(id = id_carpeta)
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
        'analisis' : Analisis.objects.filter(carpeta__in = carpetas)
    }
    return render(request, "analisis/resultados.html",context=context) 


@login_required
def resultado(request, id_analisis):

    #aca se tiene que hacer el proceso de analisis y la creacion de los objetos resultado?
    
    analisis = Analisis.objects.get(id = id_analisis)
    resultados = Resultado.objects.filter(analisis = analisis)
    context = {
        'analisis' : analisis,
        'aplicacion' : analisis.modelo.aplicacion,
        'resultados' : resultados,
    }
    return render(request, "analisis/resultado.html", context= context) 




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
    archivo.delete()
    response = redirect('/carpeta/'+str(carpeta.id))
    return response


@login_required
def borrar_resultado(request, id_analisis):
    #TODO
    analisis = Analisis.objects.get(id = id_analisis)
    return 1