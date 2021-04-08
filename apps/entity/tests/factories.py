import factory
from apps.entity.models import Entity


class EntityFactory(factory.django.DjangoModelFactory):
    name = "an entity"
    description = "this entity represents something in a text"
    should_anonimyzation = False
    should_trained = False
    enable_multiple_selection = False

    class Meta:
        model = Entity
