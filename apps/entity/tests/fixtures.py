import os
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_UNDERLINE


class ActFileFixture:
    def __init__(self, file_name, *, type="docx"):
        self.file_name = file_name
        document = DocxDocument(file_name)
        contents = create_dummy_sentence()
        document = document.build(contents)
        self.output_dir = document.create()

    def build_in_memory_uploaded_file(self, opened_file, file_name="test_file", file_field="file"):
        return InMemoryUploadedFile(
            opened_file.buffer, file_field, file_name, None, None, opened_file.buffer.tell(), None
        )


def create_dummy_sentence():
    header_paragraphs = [
        "2019 - Año del 25º Aniversario del reconocimiento de la autonomía de la Ciudad de Buenos Aires",
        "JUZGADO DE 1RA INSTANCIA EN LO PENAL CONTRAVENCIONAL Y DE FALTAS N°10   SECRETARÍA UNICA",
        "Ordena trabar embargo sobre cuenta bancaria",
        "CUIJ: IPP J-01-00006472-1/2021-0",
        "Actuación Nro: 18236125/2021",
    ]
    footer_paragraphs = [
        "Juzgado PCyF Nº 10 - Tacuarí 138, 7º Piso - juzcyf10@jusbaires.gob.ar - 4014-6821/20 - @jpcyf10"
    ]
    topic_section = (
        {
            "heading": "ORDENA EMBARGO PREVENTIVO\n",
            "paragraphs": ["Ordena trabar embargo sobre cuenta bancaria"],
            "date_and_place": "Buenos Aires, 18 de febrero de 2021.",
        },
    )
    body_sections = [
        {
            "heading": "ANTECEDENTES\n",
            "paragraphs": [
                "    El pasado 25 de enero de 2021 decidí revocar la suspensión del proceso a prueba concedida al acusado el 03/12/2020 en el marco de este caso penal.",
                "    En razón de ello regulé alimentos provisorios en favor de Juan Lopez, Ana Lopez , Rosario Lopez Y Agusto Lopez domiciliados junto a su madre Roberta Paz , por el monto de dos mil pesos ($2.000) mensuales, a partir del mes de Marzo y hasta tanto la justicia civil regule el régimen definitivo.\n",
                "    Esta decisión fue apelada por la defensa y finalmente el pasado 05/02/2021 la Cámara de Apelaciones la confirmó en su totalidad, venciendo el plazo para presentar recursos sin que la defensa efectuara una nueva presentación.",
                "    En función de ello, el 10/02/2021 decidí intimar al acusado a través de su defensa a fin de que acredite el cumplimiento de las obligaciones mencionadas.",
                "    En lo que aquí interesa, tambien hay que tener en cuenta que el acusado de  nacionalidad argentina, con numero de documento 11.111.111, propietario de un automovil  de marca Ford Fiesta con patente AB123CD , radicado en la dirección Chiclana 1429 , Bernal, Provincia de Buenos Aires desde hace 3 años. Las pruebas que se remiten son imagenAuto1.jpg  y videoAuto.mp4.\n",
                "    En virtud de ello, solicitó al juzgado que instrumentara las medidas necesarias para que los fondos existentes en la mencionada cuenta bancaria fueran transferidos a una cuenta bancaria a nombre de la denunciante, quien convive con los niños y niñas beneficiarios del subsidio. ",
                "    Explicó que el pedido se basaba en la inexistencia de una tarjeta de débito por parte de su asistido que le permitiera realizar la transferencia por cajero automático o por ventanilla desde cualquier sucursal de la entidad bancaria señalada, así como su incapacidad manifiesta para operar a través de los canales bancarios y electrónicos habituales para el común de las personas.",
                "    En oportunidad de expedirse, la Fiscalía refirió que estaba realizando las tareas necesarias a fin de poder retomar contacto con la víctima ya que los teléfonos aportados en la investigación se encuentran fuera del área de cobertura.",
                "    En función de ello e invocando la Convención de los Derechos del Niño manifestó que la única forma de asegurar las condiciones de vida necesarias para el desarrollo de los niños y niñas en este caso es trabando embargo en la cuenta bancaria sobre la suma existente y sobre las futuras sumas de dinero que mensualmente se acrediten en dicha cuenta, hasta tanto pueda contactarse con la denunciante.\n",
            ],
        },
        {
            "heading": "ARGUMENTOS\n",
            "paragraphs": [
                "   El pedido de embargo busca garantizar que las sumas de dinero entregadas por el Estado para la manutención y el cuidado del niño y las niñas presentes en este caso sean efectivamente utilizadas a dichos fines.",
                "   En este sentido, ya sostuve en oportunidades anteriores que las hipótesis según las cuales considero que resulta procedente el embargo, son la necesidad de asegurar el cumplimiento de la pena pecuniaria que podría imponerse al acusado en caso de recaer condena, como así también la posibilidad de garantizar la reparación del daño causado por el delito (art. 188 CPP) o la indemnización civil derivada de la deuda alimentaria (art. 343 CPP).\n",
                "   En segundo lugar, se encuentra configurado el requisito relativo al mérito sustantivo, dado que de acuerdo con la prueba señalada por la señora Fiscal en su requerimiento de juicio, se encuentran reunidos elementos suficientes como sostener la adecuada fundamentación de la acusación.",
                "   A ello debe sumarse que ya analicé previamente los antecedentes del caso y los elementos de cargo aportados por la fiscalía y en función de ello decidí obligar al acusado a que entregase a la denunciante la totalidad del dinero que reciba de ANSES en concepto de asignación por sus hijos e hijas.",
                "   Efectivamente, de la prueba aportada por la Fiscalía surge que es la denunciante quien se encuentra al cuidado exclusivo de los hijos que tiene en común con el acusado.",
                "   En tercer lugar, se encuentran suficientemente comprobados los riesgos procesales alegados por la señora Fiscal, dado que se acreditó a partir de los elementos probatorios aportados en el caso, que dicha cuenta es de exclusiva titularidad del acusado, por lo que es necesario reducir el riesgo de que pudiera disponer libremente de dicho dinero para evadir el cumplimiento de la eventual pena pecuniaria y de los demás deberes resarcitorios que pudieran surgir. ",
                "   Por lo expuesto, entiendo que la medida cautelar solicitada resulta procedente para garantizar el interés superior de los niños que resultarían víctimas del delito imputado al acusado, como así también los derechos de la denunciante.",
                "   Concretamente, voy a disponer que se trabe embargo sobre la cuenta de caja de ahorro social nro. 234521 del Banco Columbia , abierta en la Sucursal nro. 22 de la localidad de Quilmes de la Provincia de Buenos Aires, a nombre de Carlos Lopez , DNI 62.122.522, asociada a la casilla de mail carloslopes@mail.com.ar.Ademas las sumas que a futuro perciba allí el acusado en representación de sus hijos menores de edad, haciéndole saber al Banco Columbia que deberá informar mensualmente los depósitos realizados a la Fiscalía interviniente, ya que mi jurisdicción sobre el caso cesará con la remisión del caso a juicio, en virtud del estadio procesal en que nos encontramos.",
            ],
        },
    ]
    return {
        "header_paragraphs": header_paragraphs,
        "footer_paragraphs": footer_paragraphs,
        "topic_section": topic_section,
        "body_sections": body_sections,
    }


class DocxDocument:
    def __init__(self, file_name):
        self.file_name = file_name
        self.document = Document()
        section = self.document.sections[0]
        section.different_first_page_header_footer = True
        self.first_page_header = section.first_page_header
        self.first_page_footer = section.first_page_footer
        self.footer = section.footer

    def build_header(self, paragraphs):
        for index, paragraph in enumerate(paragraphs):
            if index == 0:
                self.first_page_header.add_paragraph(paragraph, style="Body Text 3")
            else:
                p = self.first_page_header.add_paragraph(style="Body Text 3")
                p.add_run(paragraph).bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    def build_footer(self, paragraphs):
        for paragraph in paragraphs:
            self.first_page_footer.add_paragraph(paragraph, style="Body Text 3")
            self.footer.add_paragraph(paragraph, style="Body Text 3")

    def build_topic_section(self, content):
        h = self.document.add_heading("", 1)
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        h_run = h.add_run(content["heading"])
        h_run.underline = WD_UNDERLINE.SINGLE
        for paragraph in content["paragraphs"]:
            p = self.document.add_paragraph(style="Body Text 2")
            p_run = p.add_run(paragraph)
            p_run.bold = True
            p_run.italic = True
            p_run.underline = WD_UNDERLINE.SINGLE
        self.document.add_paragraph(content["date_and_place"], style="Body Text 2")

    def build_body_section(self, body_sections):
        for body_section in body_sections:
            h = self.document.add_heading("", 1)
            h.alignment = WD_ALIGN_PARAGRAPH.LEFT
            h_run = h.add_run(body_section["heading"])
            h_run.underline = WD_UNDERLINE.SINGLE
            [self.document.add_paragraph(paragraph, style="Body Text 2") for paragraph in body_section["paragraphs"]]

    def build(self, document_data):
        """
        Given some document data, build a document in the document property and
        returns a DocxDocument instance.
        :param dummy_document: an object representing data to create a docx
        document. See the create_dummy_sentence function.
        """
        self.build_header(document_data["header_paragraphs"])
        self.build_footer(document_data["footer_paragraphs"])
        self.build_topic_section(document_data["topic_section"][0])
        self.build_body_section(document_data["body_sections"])
        return self

    def create(self):
        """
        This method expects build to have been called. Creates a file with the
        given file_name in the current directory and returns the output path.
        """
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_name)
        self.document.save(output_dir)
        return output_dir
