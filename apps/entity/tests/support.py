import os
import random
import string
from django.conf import settings


def get_test_file_dir(file_name):
    return os.path.join(settings.ACT_FILES_DIR, file_name)


def generate_random_string(string_length):
    "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(string_length))
