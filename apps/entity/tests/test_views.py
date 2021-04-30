from apps.accounts.models import User
from apps.accounts.tests.support import create_and_login_user
from apps.entity.models import Entity
from apps.entity.tests.factories import ActFactory, EntityFactory
from django.contrib.auth import authenticate, login
from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework.test import APITestCase


class EntityViewSetTest(APITestCase):
    fixtures = ["1_entity.json"]

    def setUp(self):
        self.client = Client()

    def test_an_authenticated_user_gets_an_entity_list(self):
        create_and_login_user(self.client)
        url = reverse("entity-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        entities = list(Entity.objects.all())
        self.assertEquals(len(response.data), len(entities))

    def test_an_unauthenticated_user_cannot_get_an_entity_list(self):
        url = reverse("entity-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)


class ActViewSetTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.acts = ActFactory.create_batch(10)

    def test_an_authenticated_user_gets_an_act_list(self):
        create_and_login_user(self.client)
        url = reverse("act-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), len(self.acts))

    def test_an_unauthenticated_user_cannot_get_an_act_list(self):
        url = reverse("act-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)
