import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.entity.models import Act, Entity


class EntityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entity

    name = "an entity"
    description = "this entity represents something in a text"
    should_anonimyzation = False
    should_trained = False
    enable_multiple_selection = False


class ActFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Act

    text = "a text"
    file = SimpleUploadedFile("a-file.docx", b"file contents.")
    offset_header = 0
