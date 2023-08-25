from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Carpeta, Archivo, Analisis, Aplicacion, Resultado

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
    return render(request, "analisis/config.html") 

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
    context = {
        "carpeta": carpeta,
        "archivos": Archivo.objects.filter(carpeta = carpeta)
    }
    return render(request, "analisis/carpeta.html", context=context) 

@login_required
def aplicacion(request, id_app):
    context = {
        "aplicacion": Aplicacion.objects.get(id = id_app)
    }
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
    #en algun momento antes de entrar aca se crearia el objeto analisis
    
    analisis = Analisis.objects.get(id = id_analisis)
    resultados = Resultado.objects.filter(analisis = analisis)
    context = {
        'analisis' : analisis,
        'aplicacion' : analisis.aplicacion,
        'resultados' : resultados,
    }
    return render(request, "analisis/resultado.html", context= context) 