import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import tag
from apps.entity.models import Act, Entity
from .factories import ActFactory, EntityFactory


class EntityTest(TestCase):
    def valid_attrs(self):
        return {
            "name": "some name",
            "description": "some description",
            "should_anonimyzation": False,
            "should_trained": False,
            "enable_multiple_selection": False,
        }

    def update_attrs(self):
        return {
            "name": "some updated name",
            "description": "some updated description",
            "should_anonimyzation": True,
            "should_trained": True,
            "enable_multiple_selection": True,
        }

    def invalid_attrs(self):
        return {
            "name": None,
            "description": None,
            "should_anonimyzation": None,
            "should_trained": None,
            "enable_multiple_selection": None,
        }

    def test_create_with_valid_args(self):
        entity = EntityFactory(**self.valid_attrs())
        self.assertIsNotNone(entity.id)

    @unittest.expectedFailure
    def test_create_with_invalid_args(self):
        EntityFactory(**self.invalid_attrs())

    def test_update_with_valid_args(self):
        entity = EntityFactory.create()
        updated_entity_id = Entity.objects.filter(id=entity.id).update(**self.valid_attrs())
        self.assertIsNotNone(updated_entity_id)

    @unittest.expectedFailure
    def test_update_with_invalid_args(self):
        entity = EntityFactory.create()
        Entity.objects.filter(id=entity.id).update(**self.invalid_attrs())

    def test_delete_entity(self):
        entity = EntityFactory.create()
        deleted_objects, _ = entity.delete()
        self.assertEquals(deleted_objects, 1)


class ActTest(TestCase):
    def valid_attrs(self):
        return {
            "text": "some text",
            "file": SimpleUploadedFile("some-file.docx", b"some file contents."),
            "offset_header": 0,
        }

    def update_attrs(self):
        return {
            "text": "some updated text",
            "file": SimpleUploadedFile("some-updated-file.docx", b"some updated file contents."),
            "offset_header": 500,
        }

    def invalid_attrs(self):
        return {
            "text": None,
            "file": None,
            "offset_header": None,
        }

    def test_create_with_valid_args(self):
        act = ActFactory(**self.valid_attrs())
        self.assertIsNotNone(act.id)

    @unittest.expectedFailure
    def test_create_with_invalid_args(self):
        ActFactory(**self.invalid_attrs())

    def test_update_with_valid_args(self):
        act = ActFactory.create()
        updated_act_id = Act.objects.filter(id=act.id).update(**self.valid_attrs())
        self.assertIsNotNone(updated_act_id)

    @unittest.expectedFailure
    def test_update_with_invalid_args(self):
        act = ActFactory.create()
        Act.objects.filter(id=act.id).update(**self.invalid_attrs())

    def test_delete_entity(self):
        act = ActFactory.create()
        deleted_objects, _ = act.delete()
        self.assertEquals(deleted_objects, 1)
