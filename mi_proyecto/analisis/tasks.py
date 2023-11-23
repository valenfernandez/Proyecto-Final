from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task, Celery
from .nlp import procesar_analisis
from .models import Analisis
from django.core import serializers
from django.contrib.auth.models import User
celery = Celery('tasks', broker='amqp://guest@localhost//')

# Task imports
import time

PROGRESS_STATE = 'PROGRESS'

@shared_task(bind=True)
def comenzar_celery(self, id_analisis, data): #ESTO NO SERIA ASI CREO PORQUE NO ESTA ACTUALIZANDO EL ESTADO. No se si se puede pasar solo el analisis y despues tener el list of work con ese solo o como funciona. 
    analisis = Analisis.objects.get(id = id_analisis)
    user = serializers.deserialize("json", data)
    user = list(user)
    user = user[0]
    user = user.object
    print('Download: Task started')
    try:
        procesar_analisis(analisis= analisis, user=user)
    except Exception as exc:
        print(exc)
        print('Download: Task failed')
        raise self.retry(exc=exc)
    return 'work is complete'

def do_work_item(self, work_item, list_of_work):
    self.update_state(
        state=PROGRESS_STATE,
        meta={
            'current': work_item,
            'total': len(list_of_work),
        }
    )
    print("work item: ", work_item)
    # procesar_analisis(analisis= analisis)