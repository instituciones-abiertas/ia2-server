from factory import SubFactory
from factory.django import DjangoModelFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.entity.models import Act, ActStats, Entity


class EntityFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    name = "an entity"
    description = "this entity represents something in a text"
    should_anonimyzation = False
    should_trained = False
    enable_multiple_selection = False


class ActFactory(DjangoModelFactory):
    class Meta:
        model = Act

    text = "a text"
    file = SimpleUploadedFile("a-file.docx", b"file contents.")
    offset_header = 0


class ActStatsFactory(DjangoModelFactory):
    class Meta:
        model = ActStats

    act = SubFactory(ActFactory)
