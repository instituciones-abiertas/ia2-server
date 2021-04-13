import json
from faker.providers import BaseProvider
from faker import Faker


class EntityProvider(BaseProvider):
    def get_entity(self, entity_name):
        entity = None
        entities = []
        with open("apps/entity/fixtures/1_entity.json") as entities_json:
            entities = [e["fields"] for e in json.load(entities_json)]
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
