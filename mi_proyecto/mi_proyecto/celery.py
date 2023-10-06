from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, task
from celery.result import AsyncResult

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

app = Celery('mi_proyecto')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@task
def do_work(self, list_of_work, progress_observer):
    total_work_to_do = len(list_of_work)
    for i, work_item in enumerate(list_of_work):
        do_work_item(work_item)
        # tell the progress observer how many out of the total items we have processed
        progress_observer.set_progress(i, total_work_to_do)
    return 'work is complete'

task.update_state(
    state=PROGRESS_STATE,
    meta={
        'current': current,
        'total': total,
    }
)

result = AsyncResult(task_id)
print(result.state)  # will be set to PROGRESS_STATE
print(result.info)  # metadata will be here