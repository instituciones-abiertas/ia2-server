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


class AssignNerIndexesTest(TestCase):
    """Tests for the assign_ner_indexes utility function."""

    def setUp(self):
        from apps.entity.utils.vistas import assign_ner_indexes
        self.assign_ner_indexes = assign_ner_indexes
        self.act = ActFactory(text="John Doe went to Buenos Aires. Jane Smith met John Doe in Buenos Aires.")
        self.entity_per = EntityFactory(name="PER", description="Person")
        self.entity_loc = EntityFactory(name="LOC", description="Location")

    def _create_occurrence(self, entity, text, start, end, deleted=False):
        return OcurrencyEntity.objects.create(
            act=self.act,
            entity=entity,
            text=text,
            startIndex=start,
            endIndex=end,
            should_anonymized=True,
            human_marked_ocurrency=False,
            human_deleted_ocurrency=deleted,
        )

    def test_same_text_same_entity_gets_same_index(self):
        """Two occurrences of 'John Doe' (PER) should get the same ner_index."""
        occ1 = self._create_occurrence(self.entity_per, "John Doe", 0, 8)
        occ2 = self._create_occurrence(self.entity_per, "John Doe", 47, 55)

        self.assign_ner_indexes(self.act)

        occ1.refresh_from_db()
        occ2.refresh_from_db()
        self.assertEqual(occ1.ner_index, occ2.ner_index)
        self.assertEqual(occ1.ner_index, 1)

    def test_different_text_same_entity_gets_different_index(self):
        """'John Doe' and 'Jane Smith' (both PER) should get different indexes."""
        occ1 = self._create_occurrence(self.entity_per, "John Doe", 0, 8)
        occ2 = self._create_occurrence(self.entity_per, "Jane Smith", 31, 41)

        self.assign_ner_indexes(self.act)

        occ1.refresh_from_db()
        occ2.refresh_from_db()
        self.assertNotEqual(occ1.ner_index, occ2.ner_index)
        self.assertEqual(occ1.ner_index, 1)
        self.assertEqual(occ2.ner_index, 2)

    def test_same_text_different_entity_gets_independent_index(self):
        """Same text under different entity types gets index 1 for each type."""
        occ_per = self._create_occurrence(self.entity_per, "Buenos Aires", 22, 34)
        occ_loc = self._create_occurrence(self.entity_loc, "Buenos Aires", 59, 71)

        self.assign_ner_indexes(self.act)

        occ_per.refresh_from_db()
        occ_loc.refresh_from_db()
        self.assertEqual(occ_per.ner_index, 1)
        self.assertEqual(occ_loc.ner_index, 1)

    def test_case_insensitive_grouping(self):
        """'John Doe' and 'john doe' should get the same ner_index."""
        occ1 = self._create_occurrence(self.entity_per, "John Doe", 0, 8)
        occ2 = self._create_occurrence(self.entity_per, "john doe", 47, 55)

        self.assign_ner_indexes(self.act)

        occ1.refresh_from_db()
        occ2.refresh_from_db()
        self.assertEqual(occ1.ner_index, occ2.ner_index)

    def test_deleted_occurrences_are_excluded(self):
        """Deleted occurrences should not receive a ner_index."""
        occ1 = self._create_occurrence(self.entity_per, "John Doe", 0, 8)
        occ_deleted = self._create_occurrence(self.entity_per, "Jane Smith", 31, 41, deleted=True)

        self.assign_ner_indexes(self.act)

        occ1.refresh_from_db()
        occ_deleted.refresh_from_db()
        self.assertEqual(occ1.ner_index, 1)
        self.assertIsNone(occ_deleted.ner_index)

    def test_indexes_are_sequential_by_position(self):
        """Indexes should be assigned in order of first appearance (startIndex)."""
        # Jane appears first positionally
        occ_jane = self._create_occurrence(self.entity_per, "Jane Smith", 0, 10)
        occ_john = self._create_occurrence(self.entity_per, "John Doe", 20, 28)

        self.assign_ner_indexes(self.act)

        occ_jane.refresh_from_db()
        occ_john.refresh_from_db()
        self.assertEqual(occ_jane.ner_index, 1)
        self.assertEqual(occ_john.ner_index, 2)

    def test_no_occurrences(self):
        """Calling assign_ner_indexes on an act with no occurrences should not error."""
        empty_act = ActFactory(text="No entities here.")
        self.assign_ner_indexes(empty_act)  # Should not raise

    def test_multiple_entity_types_indexed_independently(self):
        """Each entity type maintains its own index counter."""
        occ_per1 = self._create_occurrence(self.entity_per, "John Doe", 0, 8)
        occ_loc1 = self._create_occurrence(self.entity_loc, "Buenos Aires", 22, 34)
        occ_per2 = self._create_occurrence(self.entity_per, "Jane Smith", 31, 41)
        occ_loc2 = self._create_occurrence(self.entity_loc, "Córdoba", 42, 49)

        self.assign_ner_indexes(self.act)

        occ_per1.refresh_from_db()
        occ_per2.refresh_from_db()
        occ_loc1.refresh_from_db()
        occ_loc2.refresh_from_db()

        # PER: John Doe=1, Jane Smith=2
        self.assertEqual(occ_per1.ner_index, 1)
        self.assertEqual(occ_per2.ner_index, 2)
        # LOC: Buenos Aires=1, Córdoba=2
        self.assertEqual(occ_loc1.ner_index, 1)
        self.assertEqual(occ_loc2.ner_index, 2)

    def test_recalculation_updates_existing_indexes(self):
        """Running assign_ner_indexes twice should produce the same result."""
        occ1 = self._create_occurrence(self.entity_per, "John Doe", 0, 8)
        occ2 = self._create_occurrence(self.entity_per, "Jane Smith", 31, 41)

        self.assign_ner_indexes(self.act)
        self.assign_ner_indexes(self.act)

        occ1.refresh_from_db()
        occ2.refresh_from_db()
        self.assertEqual(occ1.ner_index, 1)
        self.assertEqual(occ2.ner_index, 2)