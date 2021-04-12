from apps.accounts.models import User
from apps.accounts.factories import UserFactory
from apps.entity.tests.factories import EntityFactory
from django.contrib.auth import authenticate, login
from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework.test import APITestCase


class EntityViewSetTest(APITestCase):
    def setUp(self):
        self.entities = EntityFactory.create_batch(10)

        user = UserFactory.create()
        self.user_password = "examplepassword"
        user.set_password(self.user_password)
        user.save()
        self.assertTrue(user.check_password(self.user_password))

        self.user = user
        self.client = Client()

    @tag("wip")
    def test_an_authenticated_user_gets_an_entity_list(self):
        self.client.login(username=self.user.get_username(), password=self.user_password)
        url = reverse("entity-list")
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), len(self.entities))
