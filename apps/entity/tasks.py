import string

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery_once import QueueOnce

from celery import shared_task
from liberajus.celery import app
import time

celery = app

@shared_task
def train_model():
    print("Starting async task...")
    time.sleep(1)
    model_path = f'{settings.MODELS_PATH}/test_model/test.txt'

    model = None
    with open(model_path, 'r') as reader:
        model = reader.readlines()

    line_to_change = int(model[2])
    model[line_to_change] = f'{line_to_change}.' + f'Call number {line_to_change - 3} changed this line.\n '
    increased_line_to_change = line_to_change + 1
    model[2] = f'{str(increased_line_to_change)}\n'

    with open(model_path, 'w') as reader:
        model = reader.writelines(model)

    print("RESULT MODEL")
    print(model)

    return f'wait: secs and train, task Done!'
