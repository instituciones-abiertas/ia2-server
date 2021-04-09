from django.test import Client, TestCase, tag
from apps.accounts.models import User
from apps.accounts.factories import UserFactory
from django.contrib.auth import authenticate, login


@tag("wip")
class EntityViewSetTest(TestCase):
    def setUp(self):
        user = UserFactory.create()
        self.user_password = "example password"
        user.set_password(self.user_password)
        self.user = user
        self.client = Client()

    def test_one(self):
        r = self.client.post(
            "/api/token/",
            {"username": self.user.email, "password": self.user_password},
            content_type="application/json",
        )
        print("auth response")
        print(r)
        response = self.client.get("/api/entity/")
        print("response")
        print(response)

        self.assertEquals(True, True)
