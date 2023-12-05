from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="analisis-home"),
    path("principal", views.principal, name="analisis-principal"),
    path("config", views.config, name="analisis-config"),
    path("carpetas", views.carpetas, name="analisis-carpetas"),
    path("carpeta/<id_carpeta>", views.carpeta, name="analisis-carpeta"),
    path("aplicacion/<id_app>", views.aplicacion, name="analisis-aplicacion"),
    path("resultados", views.resultados, name="analisis-resultados"),
    path("resultado/<id_analisis>", views.resultado, name="analisis-resultado"),
    path("nueva_carpeta", views.nueva_carpeta, name="analisis-nueva_carpeta"),
    path("borrar_archivo/<id_archivo>", views.borrar_archivo, name="analisis-borrar_archivo"),
    path("borrar_carpeta/<id_carpeta>", views.borrar_carpeta, name="analisis-borrar_carpeta"),
    path("borrar_analisis/<id_analisis>", views.borrar_analisis, name="analisis-borrar_analisis"),
    path("descargar_resultados_entidades/<id_analisis>/<id_archivo>", views.descargar_resultados_entidades, name="analisis-descargar_resultados_entidades"),
    path("descargar_resultados_clasificador/<id_analisis>", views.descargar_resultados_clasificador, name="analisis-descargar_resultados_clasificador"),
    path("procesar/<id_analisis>", views.procesar, name = "analisis-procesar"),
    path("crear_wordcloud/<id_analisis>", views.crear_wordcloud, name = "analisis-crear_wordcloud"),
    path("comenzar_tarea_celery/<id_analisis>", views.comenzar_tarea_celery, name="analisis-comenzar_tarea_celery"),
    path("procesar/obtener_progreso_tarea_celery/<task_id>", views.get_progress, name="analisis-get_progress"),
]
