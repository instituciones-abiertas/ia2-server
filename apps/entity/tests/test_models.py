import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag
from apps.entity.models import Act, ActStats, Entity, LearningModel, OcurrencyEntity
from .factories import ActFactory, ActStatsFactory, EntityFactory, LearningModelFactory, EntityOccurrenceFactory


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
        updated_entity_id = Entity.objects.filter(id=entity.id).update(**self.update_attrs())
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
        updated_act_id = Act.objects.filter(id=act.id).update(**self.update_attrs())
        self.assertIsNotNone(updated_act_id)

    @unittest.expectedFailure
    def test_update_with_invalid_args(self):
        act = ActFactory.create()
        Act.objects.filter(id=act.id).update(**self.invalid_attrs())

    def test_delete_entity(self):
        act = ActFactory.create()
        deleted_objects, _ = act.delete()
        self.assertEquals(deleted_objects, 1)


class ActStatsTest(TestCase):
    def valid_attrs(self):
        return {
            "act_id": ActFactory(
                text="some text",
                file=SimpleUploadedFile("some-file.docx", b"some file contents."),
                offset_header=0,
            ).id,
        }

    def update_attrs(self):
        return {
            "act_id": ActFactory(
                text="some updated text",
                file=SimpleUploadedFile("some-updated-file.docx", b"some updated file contents."),
                offset_header=0,
            ).id,
        }

    def invalid_attrs(self):
        return {
            "act_id": None,
        }

    def test_create_with_valid_args(self):
        act_stats = ActStatsFactory(**self.valid_attrs())
        self.assertIsNotNone(act_stats.act_id)

    def test_create_with_invalid_args(self):
        act_stats = ActStatsFactory(**self.invalid_attrs())
        self.assertIsNone(act_stats.act_id)

    def test_update_with_valid_args(self):
        act_stats = ActStatsFactory.create()
        updated_act_stats_id = ActStats.objects.filter(act_id=act_stats.act_id).update(**self.update_attrs())
        self.assertIsNotNone(updated_act_stats_id)

    @unittest.expectedFailure
    def test_update_with_invalid_args(self):
        act_stats = ActStatsFactory.create()
        ActStats.objects.filter(id=act_stats.act_id).update(**self.update_attrs())

    def test_delete_entity(self):
        act_stats = ActStatsFactory.create()
        deleted_objects, _ = act_stats.delete()
        self.assertEquals(deleted_objects, 1)


class OcurrencyEntityTest(TestCase):
    def valid_attrs(self):
        return {
            "act": ActFactory(),
            "startIndex": 0,
            "endIndex": 9,
            "entity": EntityFactory(),
            "should_anonymized": False,
            "text": "some text",
            "human_marked_ocurrency": False,
            "human_deleted_ocurrency": False,
        }

    def update_attrs(self):
        return {
            "act": ActFactory(),
            "startIndex": 45,
            "endIndex": 55,
            "entity": EntityFactory(),
            "should_anonymized": True,
            "text": "some updated text",
            "human_marked_ocurrency": True,
            "human_deleted_ocurrency": True,
        }

    def invalid_attrs(self):
        return {
            "act": None,
            "startIndex": None,
            "endIndex": None,
            "entity": None,
            "should_anonymized": None,
            "text": None,
            "human_marked_ocurrency": None,
            "human_deleted_ocurrency": None,
        }

    def test_create_with_valid_args(self):
        occurrency = EntityOccurrenceFactory(**self.valid_attrs())
        self.assertIsNotNone(occurrency.id)

    @unittest.expectedFailure
    def test_create_with_invalid_args(self):
        EntityOccurrenceFactory(**self.invalid_attrs())

    def test_update_with_valid_args(self):
        occurrency = EntityOccurrenceFactory.create()
        updated_occurrency_id = OcurrencyEntity.objects.filter(id=occurrency.id).update(**self.update_attrs())
        self.assertIsNotNone(updated_occurrency_id)

    @unittest.expectedFailure
    def test_update_with_invalid_args(self):
        occurrency = EntityOccurrenceFactory.create()
        OcurrencyEntity.objects.filter(id=occurrency.id).update(**self.invalid_attrs())

    def test_delete_entity(self):
        occurrency = EntityOccurrenceFactory.create()
        deleted_objects, _ = occurrency.delete()
        self.assertEquals(deleted_objects, 1)


class LearningModelTest(TestCase):
    def valid_attrs(self):
        return {
            "name_subject": "some subject name",
        }

    def update_attrs(self):
        return {
            "name_subject": "some updated subject name",
        }

    def invalid_attrs(self):
        return {
            "name_subject": None,
        }

    def test_create_with_valid_args(self):
        learning_model = LearningModelFactory(**self.valid_attrs())
        self.assertIsNotNone(learning_model.id)

    @unittest.expectedFailure
    def test_create_with_invalid_args(self):
        LearningModelFactory(**self.invalid_attrs())

    def test_update_with_valid_args(self):
        learning_model = LearningModelFactory.create()
        updated_learning_model_id = LearningModel.objects.filter(id=learning_model.id).update(**self.update_attrs())
        self.assertIsNotNone(updated_learning_model_id)

    @unittest.expectedFailure
    def test_update_with_invalid_args(self):
        learning_model = LearningModelFactory.create()
        LearningModel.objects.filter(id=learning_model.id).update(**self.invalid_attrs())

    def test_delete_entity(self):
        learning_model = LearningModelFactory.create()
        deleted_objects, _ = learning_model.delete()
        self.assertEquals(deleted_objects, 1)
