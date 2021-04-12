from apps.accounts.models import User
from apps.accounts.tests.support import create_and_login_user
from apps.entity.tests.factories import EntityFactory
from django.contrib.auth import authenticate, login
from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework.test import APITestCase


class EntityViewSetTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.entities = EntityFactory.create_batch(10)
        create_and_login_user(self.client)

    def test_an_authenticated_user_gets_an_entity_list(self):
        url = reverse("entity-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), len(self.entities))
