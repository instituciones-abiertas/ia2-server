# IA² | Backend

<p align="center">
  <a target="_blank" rel="noopener noreferrer">
    <img width="220px" src="ia2/static/images/ia2-logo.png" alt="IA²" />
  </a>
</p>
<h4 align="center">Servidor del proyecto IA²</h4>

---

<p align="center" style="margin-top: 14px;">
  <a
    href="https://github.com/instituciones-abiertas/ia2-server/blob/main/LICENSE"
  >
    <img
      src="https://img.shields.io/badge/License-GPL%20v3-blue.svg"
      alt="License" height="20"
    >
  </a>
  <a
    href="https://github.com/instituciones-abiertas/ia2-server/blob/main/CODE_OF_CONDUCT.md"
  >
    <img
      src="https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg"
      alt="Contributor Covenant" height="20"
    >
  </a>
</p>

## Stack Tecnológico

+ [Django 2.2.5](https://docs.djangoproject.com/en/3.1/releases/2.2/)
+ [Docker](https://docs.docker.com/)
+ [Docker Compose](https://docs.docker.com/compose/#compose-documentation)

## Ambiente de desarrollo

A continuación se detallan las instrucciones a seguir para configurar el ambiente de desarrollo.

Realizar una copia del archivo `.env.example` y renombrarlo a `.env`. Luego, será necesario configurar las variables de ambiente. A continuación una breve guía sobre los valores que intervienen.

### Variables de ambiente

#### Bases de datos

> MAIN es la base de datos principal, donde se registran los modelos de dominio.

+ `IA2_MAIN_DB_USER`: nombre de usuarix para acceder a la base de datos principal
+ `IA2_MAIN_DB_PASS`: contraseña de acceso a la base de datos principal
+ `IA2_MAIN_DB_ROOT_PASS`: nombre de usuarix para la cuenta root. Generalmente es `root`.
+ `IA2_MAIN_DB_NAME`: nombre de la base de datos principal
+ `IA2_MAIN_DB_PORT`: puerto de la base de datos principal

> DATA es la base de datos donde se registra la extracción de datos.

+ `IA2_DB_DATA_USER`: nombre de usuarix para acceder a la base de extracción de datos
+ `IA2_DB_DATA_PASS`: contraseña de acceso a la base de extracción datos
+ `IA2_DB_DATA_ROOT_PASS`: nombre de usuarix para la cuenta root. Generalmente es `root`.
+ `IA2_DB_DATA_NAME`: nombre de la base de extracción de datos
+ `IA2_DB_DATA_PORT`: puerto de la base de extracción datos

#### Publicador

> Utilizamos la librería [`publicador`](https://github.com/Cambalab/publicador) para subir archivos a diferentes servicios de cloud storage.

+ `PUBLICADOR_CLOUD_STORAGE_PROVIDER`: declara la estrategia de storage. Las opciones disponibles son : `dropbox`, `drive`, `both`.
+ `PUBLICADOR_CLOUDFOLDER_STORE`: declara el directorio donde se guardarán los archivos en el serrvicio de cloud storage.
+ `PUBLICADOR_DROPBOX_TOKEN_APP`: declara el token de dropbox para la autenticación.
+ `PUBLICADOR_CREDENTIALS_DRIVE_PATH`: declara la ruta hacia el archivo de credenciales de Google Drive. Más información sobre el archivo de credenciales [aquí](https://developers.google.com/drive/api/v3/quickstart/go).

#### LibreOffice

> Utilizamos la librería [oodocument](https://github.com/Cambalab/oodocument) para realizar anonimización en documentos y para operaciones de conversión de archivos.

+ `LIBREOFFICE_HOST`: host del proceso headless de libreoffice
+ `LIBREOFFICE_PORT`: puerto del proceso headless de libreoffice
+ `OODOCUMENT_NEIGHBOR_CHARS_SCAN`: máxima tolerancia de caracteres en búsquedas de texto

#### Sentry

> Utilizamos Sentry para el reporte de errores.

+ `SENTRY_DSN`: url del servicio de Sentry.
+ `SENTRY_RELEASE`: setea el ambiente de Sentry (`staging`, `demo`, `prod`, `qa`, etc...)

#### Spacy Model

+ `IA2_MODEL_FILE`: ruta o url del modelo de Spacy a utilizar. Los modelos son archivos `.tar.gz` construídos con la [línea de comandos de IA²](link-aquí). Las rutas pueden declararse de forma relativa o absoluta hacia el archivo `.tar.gz`. Ejemplos: `../../models/my-model.tar.gz`, `https://my-model-repository.coop/model_1.0.tar.gz`. El directorio `custom_models` se puede utilizar para almacenar los modelos sin ser añadidos al tracking de `.git` *(recomendado si utiliza Docker para el ambiente de desarrollo, ver la siguiente sección)*.
+ `IA2_TEST_MODEL_FILE`: simil a `IA2_MODEL_FILE`, pero el modelo en ésta variable se utiliza únicamente durante las pruebas.
#### Otras

+ `IA2_DISABLED_ENTITIES`: lista de entidades que serán ignoradas por el servidor
+ `IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION`: habilita extracción de headers de documentos
+ `USE_MULTIPLE_SELECTION_FROM_BEGINNING`: habilita la búsqueda de entidades luego de la predicción del modelo estadístico, de esta manera se utilizan las entidades detectadas para buscarlas en el resto del documento en caso de que no hayan sido detectadas aún. Las entidades que se buscarán son las que su tipo de entidad está habilitada para la búsqueda por selección múltiple.

### Precommit

Utilizamos flake para mantener la consistencia de estilo de código. Para inicializar pre-commit en el repositorio utilizar el siguiente comando:

```bash
pre-commit install
```

### Ambiente de desarrollo utilizando virtualenv

+ [`python 3.x`](https://www.python.org/downloads/)
+ [`mysql-server`](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-es)
+ [`mysql-client`](https://www.configserverfirewall.com/ubuntu-linux/ubuntu-install-mysql-client/)
+ [`virtualenv`](https://virtualenv.pypa.io/en/latest/)
+ [`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/)

#### Ambiente virtual

Una vez instaladas las dependencias, crear un ambiente con `virtualenv`:

```bash
mkvirtualenvwrapper ia2-server
```

El siguiente script actualiza las variables de ambiente de archivo `.env` cada vez que se inicie un workspace de trabajo de `virtualenv`.

```bash
echo 'source .env' >> $WORKON_HOME/postactivate
```

Asignar el ambiente de trabajo creado anteriormente:

```bash
workon ia2-server
# Luego compruebe que las variables de ambiente están disponibles en su terminal
echo $DJANGO_SETTINGS_MODULE
# ia2.settings.local
```

#### Instalación

Instalar requerimientos y dependencias:

```bash
cd requirements
pip install -r local.txt
```

#### Configuración de base de datos

Crear las bases de datos

```bash
mysqladmin --user=root --password=$IA2_MAIN_DB_ROOT_PASS create $IA2_MAIN_DB_NAME
mysqladmin --user=root --password=$IA2_DB_DATA_ROOT_PASS create $IA2_DB_DATA_NAME
```

Correr las migraciones

```bash
make django-migrate
```

#### Comandos útiles

Mostrar todos los comandos.

```bash
make help
```

Borrar la base de datos.

```bash
make nuke
```

Resetea el ambiente local. Re-instala las dependencias y corre las migraciones. Útil cuando se testea una nueva rama o se cambia de rama.

```bash
make reset
```

Resetea el ambiente completo. Corre `reset` y carga los fixtures iniciales.

```bash
make nuke-reset
```

Corre todos los tests.

```bash
make test
```

Corre los tests tagueados con `wip`. Útil cuando se trabaja en un test particular.

```bash
make test.wip
```

Inicia una console interactiva de Python.

```bash
make shell
```

Compilar mensajes de internacionalización. Cada vez que realicen cambios en las traducciones será necesario re-compilar los archivos `.po` con el siguiente comando.

```bash
make django-compile-messages
```

Si realiza cambios en cualquiera de los fixtures, puede re-inicializarlos con el siguiente comando.

```bash
make django-load-fixtures
```

Crear superuser de Django. El comando inicia los pasos que lo guiarán para crear un superusuario.

```bash
make django-createsuperuser
```

#### Comando estadisticas de las entidades

> Permite generar un archivo CSV con estadísticas de las entidades procesadas por el sistema

- Ayuda: `make entity-stats ARGS="--help"`
- Completas `make entity-stats`
- Por fecha `make entity-stats ARGS="--start_date 10-10-2001 --end_date 10-10-2021"`

El documento generado tendrá este formato de nombre: `entity_stats_[start_date]-to-[end_date].csv`

> Ej: `entity_stats_20-05-2021-to-10-09-2021.csv`

### Herramientas de debugging

Es posible inciar el servidor de manera tal de poder utilizar herramientas de debugging como Wekzeug y/o PyInstrument.

+ [`Werkzeug:`](https://werkzeug.palletsprojects.com/en/0.15.x/tutorial/) Para desabilitar e PIN para debugging en ambientes locales, es necesario setear la siguiente variable de entorno en `.env`: `WERKZEUG_DEBUG_PIN=off`
+ [`PyInstrument:`](https://github.com/joerick/pyinstrument/) Es posible habilitar PyInstrument utilizando `ENABLE_PYINSTRUMENT=on` en `.env`. Los archivos html de PyInstrument se acceden desde `profiles/`.

Ejemplo utilizando Docker:

```bash
WERKZEUG_DEBUG_PIN=off ENABLE_PYINSTRUMENT=on python manage.py runserver_plus
```

### Ambiente de desarrollo con Docker

#### Comandos para administrar los servicios

Utilizamos el siguiente comando para construír la imagen de Docker con todas las dependencias necesarias.

> Nota: si se realizan cambios en `tasks.py`, será necesario volver a correr el comando de build.

```bash
docker-compose build
```

Utilice cualquiera de los siguientes comando para inicializar los servicios:

```bash
docker-compose up
```

Modo detached:

```bash
docker-compose up -d
```

Puede parar los servicios desde otro terminal, utilizando:

```bash
docker-compose stop
```

#### Comandos útiles a través de Docker Compose

> Los siguientes comandos asumen que los servicios de docker-compose están activos.

Es posible correr cualquiera de los comandos de `Makefile` descriptos en [*Comandos útiles*](#Comandos-útiles) desde docker compose de la siguiente manera:

```bash
docker-compose exec web <command>
```

**Ejemplo:**

```bash
docker-compose exec make shell
```

## Flujo de desarrollo

### Agregar nuevas dependencias

Se pueden agregar nuevos paquetes utilizando `pip` dentro del container

```bash
pip install <package_name>
```

Cada vez que instalamos un paquete, **debemos** obtener el *freeze* de las versiones.

```bash
pip freeze | grep <package_name>
```

Inclúya la dependencia en el archivo *requirements* que corresponda. Existen 4 tipos de archivos de *requirements*:

+ `base.txt`: dependencias utilizadas en todos los ambientes.
+ `local.txt`: dependencias utilizadas únicamente en el ambiente local de desarrollo.
+ `production.txt`: dependencias utilizadas únicamente en ambientes de producción.
+ `testing.txt`: dependencias utilizadas únicamente en ambientes de pruebas.

```bash
pip freeze | grep mysqlclient

mysqlclient==1.4.4
```

### Correr pruebas

Los comandos para correr las pruebas soportan los decorators de `django.test` para realizar filtrados o excepciones cuando se corren las pruebas. Más información sobre tags [aquí](https://docs.djangoproject.com/en/3.1/topics/testing/tools/#tagging-tests).

*Correr todas las pruebas, excepto aquellas con tag* ***skip***.

```bash
make test
```

*Correr unicamente las pruebas con tag* ***wip***.

```bash
make test.wip
```

### Agregar nuevas traducciones

Para crear nuevas traducciones en una app primero debemos verificar si en esa app existe un directorio `locale`. Si no existe, lo creamos. Luego de actualizarlos, correr el comando `make messages`.

Si simplemente estamos actualizando o agregando traducciones a una archivo existente, una vez finalizada la actualización, ejecutamos el siguiente comando.

*El siguiente comando actualiza todos los archivos `.mo` de traducciones, incluso la fecha de actualización de archivos que no sufrieron cambios. Por éste motivo es necesario verificar que no se agreguen archivos que no sufrieron cambios de traducción en un nuevp commit.*

```bash
make messages
```

## API Rest

Los servicios del backend pueden ser encontrados en [éste archivo](link-a-json) de [Insomnia](https://insomnia.rest/download/).

## Licencia

[**GNU General Public License version 3**](LICENSE)

## Contribuciones

Por favor, asegúrese de leer los [lineamientos de contribución](CONTRIBUTING.md) antes de realizar Pull Requests.
