import random
from apps.accounts.models import User
from apps.accounts.tests.support import create_and_login_user
from apps.entity.models import Entity
from apps.entity.serializers import ActSerializer, EntitySerializer, OcurrencyEntitySerializer
from apps.entity.tests.factories import ActFactory, EntityFactory, EntityOccurrenceFactory, OcurrencyEntity
from django.contrib.auth import authenticate, login
from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class EntityViewSetTest(APITestCase):
    fixtures = ["1_entity.json"]

    def setUp(self):
        self.client = Client()
        self.subject_list = Entity.objects.all()
        self.list_url = reverse("entity-list")
        self.subject = random.choice(self.subject_list)
        self.detail_url = reverse("entity-detail", args=[self.subject.id])

    def test_a_superuser_user_gets_an_entity_list(self):
        create_and_login_user(self.client)
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = EntitySerializer(self.subject_list.order_by("name"), many=True)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_an_entity_list(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_superuser_gets_a_single_entity(self):
        create_and_login_user(self.client)
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = EntitySerializer(self.subject)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_a_single_entity(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class ActViewSetTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.subject_list = ActFactory.create_batch(10)
        self.list_url = reverse("act-list")
        self.subject = random.choice(self.subject_list)
        self.detail_url = reverse("act-detail", args=[self.subject.id])

    def test_a_superuser_gets_an_act_list(self):
        create_and_login_user(self.client)
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = ActSerializer(self.subject_list, many=True)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_an_act_list(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_superuser_gets_a_single_entity(self):
        create_and_login_user(self.client)
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = ActSerializer(self.subject)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_a_single_entity(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class EntityOccurrenceTest(APITestCase):
    fixtures = ["1_entity.json", "3_acts.json", "5_ocurrences.json"]

    def setUp(self):
        self.client = Client()
        self.subject_list = OcurrencyEntity.objects.all()
        self.list_url = reverse("ocurrencyentity-list")
        self.subject = random.choice(self.subject_list)
        self.detail_url = reverse("ocurrencyentity-detail", args=[self.subject.id])

    def test_a_superuser_gets_an_entity_occurrence_list(self):
        create_and_login_user(self.client)
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = OcurrencyEntitySerializer(self.subject_list, many=True)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_an_entity_occurrence_list(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_superuser_gets_a_single_entity(self):
        create_and_login_user(self.client)
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = OcurrencyEntitySerializer(self.subject)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_a_single_entity(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
