import dateparser
from datetime import datetime
from ..utils.strings import text_es_to_num, find_replace_multi_ordered

# XXX Error conocido, veintiún no esta soportado

currentYear = str(datetime.now().year)
palabras = {"días": "", "día": "", "dias": "", "dia": "", "mes": "", "del": "", "año en curso": currentYear}

ddp = dateparser.DateDataParser(languages=["es"])


def procesa_fecha(fechaStr):
    fecha_sin_palabras = find_replace_multi_ordered(fechaStr, palabras)
    fecha_num = text_es_to_num(fecha_sin_palabras)
    fecha = ddp.get_date_data(fecha_num)
    return fecha.date_obj


if __name__ == "__main__":
    fecha_procesada = procesa_fecha("treinta y un días del mes de agosto del año en curso")
    print(fecha_procesada)
