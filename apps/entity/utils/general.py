from ..models import Entity, Act, OcurrencyEntity, LearningModel
from ..exceptions import ActNotExist, StorageFileNotExist


def check_exist_act(pk):
    try:
        return Act.objects.get(id=pk)
    except Act.DoesNotExist:
        raise ActNotExist()


def open_file(path):
    try:
        output = open(path, "rb")
    except OSError:
        raise StorageFileNotExist()
    else:
        return output


def calculate_ents_anonimyzed(arrayEnts):
    result_list = []
    type_of_ents = list(Entity.objects.all())

    for ent in type_of_ents:
        result_list.append(
            {
                "name": "Datos " + ent.name,
                "value": len(list(filter(lambda x: x.entity_id == ent.id, arrayEnts))),
            }
        )

    return result_list
