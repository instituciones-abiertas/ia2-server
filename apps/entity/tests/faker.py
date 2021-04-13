from faker.providers import BaseProvider
from faker import Faker
from .seeds import get_entities


class EntityProvider(BaseProvider):
    def get_entity(self, entity_name):
        entity = None
        entities = get_entities()
        if entity_name is not None:
            for e in entities:
                if e["name"] == entity_name:
                    entity = e
        else:
            entity = self.random_element(entities)
        return entity

    def entity_name(self, entity_name=None):
        entity = self.get_entity(entity_name)
        return entity["name"]

    def entity_description(self, entity_name=None):
        entity = self.get_entity(entity_name)
        return entity["description"]


fake = Faker(locale="es_ES")
fake.add_provider(EntityProvider)
