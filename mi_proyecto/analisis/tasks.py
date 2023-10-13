from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task


# Task imports
import time

@shared_task(bind=True)
def comenzar_celery(self, list_of_work):
    print('Download: Task started')
    for work_item in list_of_work:
        do_work_item(work_item)
    return 'work is complete'


def do_work_item(self, work_item):
	# Sleep for 100ms
    print("work item: ", work_item)
    time.sleep(1.1)
		