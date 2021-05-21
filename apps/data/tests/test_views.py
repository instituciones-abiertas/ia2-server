import io
import os
import random
import tempfile
from apps.accounts.models import User
from apps.accounts.tests.support import create_and_login_user
from apps.data.models import Lugar, Hecho, Historico
from apps.data.serializers import HechoStatsSerializer, EdadStatsSerializer, LugarStatsSerializer
from apps.data.tests.factories import HechoFactory, LugarFactory
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.test import Client, TestCase, client, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class EdadStatsViewTest(APITestCase):
    # Multi DB support
    databases = "__all__"

    def setUp(self):
        self.client = Client()
        self.stats = HechoFactory.create_batch(10)
        self.url = reverse("stats_edad")

    def test_a_superuser_user_gets_edad_stats(self):
        create_and_login_user(self.client)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Output must contain keys
        keys = ["promedio_acusadx", "promedio_victima"]
        for k in keys:
            self.assertIn(k, response.data)

        # XXX Still need  to check key values

    def test_an_unauthenticated_user_cannot_get_edad_stats(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class HechoStatsViewTest(APITestCase):
    # Multi DB support
    databases = "__all__"

    def setUp(self):
        self.client = Client()
        self.qty_hechos = 10
        self.stats = HechoFactory.create_batch(self.qty_hechos)
        self.url = reverse("stats_hecho")

    def test_a_superuser_user_gets_hecho_stats(self):
        create_and_login_user(self.client)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Output must contain keys
        keys = ["total", "violencia", "otros", "violencia_genero"]
        for k in keys:
            self.assertIn(k, response.data)

        self.assertEqual(self.qty_hechos, response.data["total"])

    def test_an_unauthenticated_user_cannot_get_hecho_stats(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class LugarStatsViewTest(APITestCase):
    # Multi DB support
    databases = "__all__"

    def setUp(self):
        self.client = Client()
        self.qty_lugares = 5
        self.qty_hechos = 10
        self.lugares = LugarFactory.create_batch(self.qty_lugares)
        self.stats = HechoFactory.create_batch(self.qty_hechos, lugares=self.lugares)
        self.url = reverse("stats_lugar")

    def test_a_superuser_user_gets_lugar_stats(self):
        create_and_login_user(self.client)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Lugares created eq array length of response
        self.assertEquals(self.qty_lugares, len(response.data))

        keys = ["nombre", "cantidad"]
        for item in response.data:
            for k in keys:
                # Output must contain keys
                self.assertIn(k, item)
            # Lugares Ocurrences equals hechos quantity
            self.assertEquals(self.qty_hechos, item["cantidad"])

    def test_an_unauthenticated_user_cannot_get_lugar_stats(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
