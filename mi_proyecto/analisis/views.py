from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request): 
    if request.user.is_authenticated and (not request.user.is_staff): 
        response = redirect('/principal')
        return response
    else: 
        return render(request, "analisis/home.html") #rarisimo, esto deberia ser analisis/home.html pero no anda asi

@login_required
def principal(request):
    return render(request, "analisis/principal.html") 

@login_required
def config(request):
    return render(request, "analisis/config.html") 

@login_required
def carpetas(request):
    return render(request, "analisis/carpetas.html") 

@login_required
def carpeta(request, id_carpeta):
    return render(request, "analisis/carpeta.html") 

@login_required
def aplicacion(request, id_app):
    return render(request, "analisis/aplicacion.html") 

@login_required
def resultados(request):
    return render(request, "analisis/resultados.html") 

@login_required
def resultado(request, id_analisis):
    return render(request, "analisis/resultados.html") 