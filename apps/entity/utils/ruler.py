patterns = [
            {"label": "LEY", "pattern": [{"LOWER": "ley"}, {"LIKE_NUM": True}]},
            {"label": "NUM_DNI", "pattern": [{"SHAPE": "d.ddd.ddd"}]},
            {"label": "NUM_DNI", "pattern": [{"SHAPE": "dd.ddd.ddd"}]},
            {"label": "NUM_DNI", "pattern": [{"SHAPE": "ddd.ddd.ddd"}]},
            {"label": "NUM_IP", "pattern": [{"SHAPE": "ddd.ddd.ddd.ddd"}]},
            {"label": "NUM_IP", "pattern": [{"SHAPE": "ddd.dd.ddd.d"}]},
            {"label": "NUM_IP", "pattern": [{"SHAPE": "ddd.dd.ddd.dd"}]},
            {"label": "NUM_TELÉFONO", "pattern": [{"SHAPE": "dd-dddd-dddd"}]},
            {"label": "NUM_TELÉFONO", "pattern": [{"SHAPE": "dddd-dddd"}]},
            {"label": "NUM_TELÉFONO", "pattern": [{"SHAPE": "dddd-ddd-dddd"}]},
            {"label": "FECHA_NUMÉRICA", "pattern": [{"SHAPE": "dd/dd/dd"}]},
            {"label": "FECHA_NUMÉRICA", "pattern": [{"SHAPE": "dd/dd"}]},
            {"label": "FECHA_NUMÉRICA", "pattern": [{"SHAPE": "d/d/dd"}]},
            # {"label": "CUIJ", "pattern": [{'LOWER': 'ipp', "OP": "?"}, {'IS_ASCII': True}]},
            {"label": "FECHA", "pattern": [{"LOWER": "a"}, {"LOWER": "los"}, {"LIKE_NUM": True}, {"LOWER": "días"}, {"LOWER": "del", "OP": "?"}, {"LOWER": "mes", "OP": "?"}, {"LOWER": "de"}, {"LOWER": {"IN": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]}}, {"POS": "ADP", "OP": "?"}, {"LIKE_NUM": True, "OP": "?"}]},
            {"label": "NACIONALIDAD", "pattern": [{"LEMMA": {"IN": ["argentino", "boliviano", "paraguayo", "colombiano", "chileno", "brasileño", "panameño", "italiano", "español", "mexicano", "ruso", "francés", "inglés", "venezolano", "estadounidense", "alemán", "chino", "indio", "cubano", "nigeriano", "polaco", "sueco", "turco", "japonés", "portugués", "iraní", "paquistaní", "costarricense", "canadiense", "marroquí", "griego", "egipcio", "coreano", "ecuatoriano", "peruano", "guatemalteco", "salvadoreño", "holandés", "dominicano"]}}]},
            {"label": "FECHA", "pattern": [{"LIKE_NUM": True}, {"POS": "ADP"}, {"LOWER": {"IN": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]}}, {"POS": "ADP", "OP": "?"},  {"LOWER": "año",  "OP": "?"}, {"LIKE_NUM": True, "OP": "?"}]},
            {"label": "NACIONALIDAD", "pattern": [{"LEMMA": {"IN": ["argentino", "boliviano", "paraguayo", "colombiano", "chileno", "brasileño", "panameño", "italiano", "español", "mexicano", "ruso", "francés", "inglés", "venezolano", "estadounidense", "alemán", "chino", "indio", "cubano", "nigeriano", "polaco", "sueco", "turco", "japonés", "portugués", "iraní", "paquistaní", "costarricense", "canadiense", "marroquí", "griego", "egipcio", "coreano", "ecuatoriano", "peruano", "guatemalteco", "salvadoreño", "holandés", "dominicano"]}}]},
            {"label": "NUM_CUIT_CUIL", "pattern":  [{"TEXT": {"REGEX": "(20|23|27|30|33)([0-9]{9}|-[0-9]{8}-[0-9]{1})"}}]},
        ]

def add_patterns(ruler):
    ruler.add_patterns(patterns)