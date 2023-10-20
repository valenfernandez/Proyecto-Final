from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task, Celery

celery = Celery('tasks', broker='amqp://guest@localhost//')

# Task imports
import time

PROGRESS_STATE = 'PROGRESS'

@shared_task(bind=True)
def comenzar_celery(self, list_of_work):
    print('Download: Task started')
    for work_item in list_of_work:
        do_work_item(self, work_item, list_of_work)
    return 'work is complete'


def do_work_item(self, work_item, list_of_work):
	# Sleep for 100ms
    self.update_state(
        state=PROGRESS_STATE,
        meta={
            'current': work_item,
            'total': len(list_of_work),
        }
    )
    print("work item: ", work_item)
    time.sleep(1.1)
		