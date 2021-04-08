from django.test import TestCase
from django.test import tag
from apps.entity.models import Entity


class EntityTest(TestCase):
    def test_list_users(self):
        print("Test")
        self.assertEqual(True, True)
