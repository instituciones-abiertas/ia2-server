import io
import os
import random
import tempfile
from apps.accounts.models import User
from apps.accounts.tests.support import create_and_login_user
from apps.entity.models import Entity
from apps.entity.serializers import ActSerializer, EntitySerializer, OcurrencyEntitySerializer
from apps.entity.tests.factories import ActFactory, EntityFactory, EntityOccurrenceFactory, OcurrencyEntity
from apps.entity.tests.fixtures import ActDocxFileFixture, ActPdfFileFixture
from apps.entity.tests.support import generate_random_string, get_test_file_dir
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import Client, TestCase, client, tag
from django.test.client import encode_multipart, RequestFactory
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
        filtered_entities = self.subject_list.exclude(name__in=settings.DISABLED_ENTITIES).order_by("name")
        serializer = EntitySerializer(filtered_entities, many=True)
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
    fixtures = ["1_entity.json"]

    def setUp(self):
        self.client = Client()
        self.subject_list = ActFactory.create_batch(10)
        self.list_url = reverse("act-list")
        self.subject = random.choice(self.subject_list)
        self.detail_url = reverse("act-detail", args=[self.subject.id])
        self.add_annotations_url = reverse("act-addAnnotations", kwargs={"pk": self.subject.id})

    def test_a_superuser_gets_an_act_list(self):
        create_and_login_user(self.client)
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = ActSerializer(self.subject_list, many=True)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_an_act_list(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_superuser_gets_a_single_act(self):
        create_and_login_user(self.client)
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = ActSerializer(self.subject)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_a_single_act(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    # Skips tests until we are able to mock the oodocument module
    @tag("skip")
    def test_a_superuser_creates_an_act_with_valid_args(self):
        create_and_login_user(self.client)
        file_name = "file.docx"
        dummy_file = ActDocxFileFixture(file_name)
        with open(dummy_file.output_dir) as opened_dummy_file:
            data = {"file": dummy_file.build_in_memory_uploaded_file(opened_dummy_file)}
            response = self.client.post(self.list_url, data=data)
            opened_dummy_file.close()
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)
            self.assertIsNotNone(response.data["id"])
            self.assertIsNotNone(response.data["text"])
            self.assertIsNotNone(response.data["ents"])
        os.remove(dummy_file.output_dir)

    def test_an_unauthenticated_user_cannot_create_an_act_with_valid_args(self):
        file_name = "file.docx"
        dummy_file = ActDocxFileFixture(file_name)
        with open(dummy_file.output_dir) as opened_dummy_file:
            data = {"file": dummy_file.build_in_memory_uploaded_file(opened_dummy_file)}
            response = self.client.post(self.list_url, data=data)
            opened_dummy_file.close()
            self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        os.remove(dummy_file.output_dir)

    def test_an_unauthenticated_user_cannot_create_an_act_with_invalid_args(self):
        response = self.client.post(self.list_url, data=None)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_superuser_cannot_create_an_act_with_an_invalid_file_format(self):
        create_and_login_user(self.client)
        file_name = "file.pdf"
        dummy_file = ActPdfFileFixture(file_name)
        with open(dummy_file.output_dir) as opened_dummy_file:
            data = {"file": dummy_file.build_in_memory_uploaded_file(opened_dummy_file)}
            response = self.client.post(self.list_url, data=data)
            opened_dummy_file.close()
            self.assertEquals(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            self.assertEquals(response.data["detail"], settings.ERROR_TEXT_FILE_TYPE)
        os.remove(dummy_file.output_dir)

    def test_a_superuser_cannot_create_an_act_with_a_long_file_name(self):
        create_and_login_user(self.client)
        file_name = "file.docx"
        dummy_file = ActDocxFileFixture(file_name)
        with open(dummy_file.output_dir) as opened_dummy_file:
            data = {
                "file": dummy_file.build_in_memory_uploaded_file(
                    opened_dummy_file, file_name=f"{generate_random_string(150)}.docx"
                )
            }
            response = self.client.post(self.list_url, data=data)
            opened_dummy_file.close()
            self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEquals(response.data["detail"], settings.ERROR_NAME_TOO_LONG)
        os.remove(dummy_file.output_dir)

    def test_a_superuser_cannot_create_an_act_with_empty_file_arg(self):
        create_and_login_user(self.client)
        response = self.client.post(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["detail"], settings.ERROR_CREATE_ACT_FILE_NOT_FOUND)

    def test_an_unauthenticated_user_cannot_add_annotations(self):
        response = self.client.post(self.add_annotations_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class EntityOccurrenceTest(APITestCase):
    fixtures = ["1_entity.json", "3_acts.json", "5_occurrences.json"]

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

    def test_a_superuser_gets_a_single_entity_occurrence(self):
        create_and_login_user(self.client)
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = OcurrencyEntitySerializer(self.subject)
        self.assertEquals(response.data, serializer.data)

    def test_an_unauthenticated_user_cannot_get_a_single_entity_occurrence(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
