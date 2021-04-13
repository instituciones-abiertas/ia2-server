from factory import Faker as FactoryFaker, LazyAttribute, LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.entity.models import Act, ActStats, Entity, OcurrencyEntity, LearningModel
from apps.entity.tests.faker import fake


class EntityFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    name = fake.entity_name()
    description = LazyAttribute(lambda o: fake.entity_description(entity_name=o.name))
    should_anonimyzation = False
    should_trained = False
    enable_multiple_selection = False


class ActFactory(DjangoModelFactory):
    class Meta:
        model = Act

    text = FactoryFaker("text", max_nb_chars=10000)
    file = SimpleUploadedFile(fake.file_name(extension="docx"), f"{fake.text(max_nb_chars=10000)}".encode())
    offset_header = 0


class ActStatsFactory(DjangoModelFactory):
    class Meta:
        model = ActStats

    act = SubFactory(ActFactory)


class OcurrencyEntityFactory(DjangoModelFactory):
    class Meta:
        model = OcurrencyEntity

    act = SubFactory(ActFactory)
    startIndex = 0
    endIndex = 20
    entity = SubFactory(EntityFactory)
    should_anonymized = False
    text = "an occurrency entity"
    human_marked_ocurrency = False
    human_deleted_ocurrency = False


class LearningModelFactory(DjangoModelFactory):
    class Meta:
        model = LearningModel

    name_subject = "a subject name"
