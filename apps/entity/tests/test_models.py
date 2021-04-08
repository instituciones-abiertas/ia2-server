import unittest
from django.test import TestCase
from django.test import tag
from apps.entity.models import Entity
from .factories import EntityFactory


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
