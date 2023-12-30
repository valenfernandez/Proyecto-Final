from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task, Celery
from nlp_component.nlp import procesar_analisis
from .models import Analisis
from django.core import serializers
from celery.exceptions import Ignore
celery = Celery('tasks', backend='redis', broker='amqp://guest@localhost//')

import time

@shared_task(bind=True)
def comenzar_celery(self, id_analisis, data):
    print("Empezando tarea de celery asíncrona. Estableciendo estado inicial.")
    self.update_state(
        state='PROGRESS',
        meta={
            'current': 1,
            'total': 10,
            'mensaje': 'Empezando análisis',
            'id_analisis': id_analisis
        }
    )
    analisis = Analisis.objects.get(id = id_analisis)
    user = serializers.deserialize("json", data)
    user = (list(user))[0].object
    try:
        print("esta por entrar al procesar analisis")
        procesar_analisis(self, analisis= analisis, user=user)
    except Exception as exc:
        analisis.delete()
        print("Tarea de celery falló. Detalle de la excepcion:", type(exc).__name__, " ", exc) 
        self.update_state(
        state='FAILED',
        meta={
            'current': 10,
            'total': 10,
            'mensaje': 'No se pudo procesar el análisis.'
        }
    )  
        raise Ignore()
    return "Finalizada tarea de celery."