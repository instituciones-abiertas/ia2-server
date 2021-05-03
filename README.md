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

#### Sentry

> Utilizamos Sentry para el reporte de errores.

+ `SENTRY_DSN`: url del servicio de Sentry.
+ `SENTRY_RELEASE`: setea el ambiente de Sentry (`staging`, `demo`, `prod`, `qa`, etc...)

#### Spacy Model

+ `IA2_MODEL_FILE`: ruta o url del modelo de Spacy a utilizar. Los modelos son archivos `.tar.gz` construídos con la [línea de comandos de IA²](link-aquí). Las rutas pueden declararse de forma relativa o absoluta hacia el archivo `.tar.gz`. Ejemplos: `../../models/my-model.tar.gz`, `https://my-model-repository.coop/model_1.0.tar.gz`. El directorio `custom_models` se puede utilizar para almacenar los modelos sin ser añadidos al tracking de `.git` *(recomendado si utiliza Docker para el ambiente de desarrollo, ver la siguiente sección)*.
+ `IA2_TEST_MODEL_FILE`: simil a `IA2_MODEL_FILE`, pero el modelo en ésta variable se utiliza únicamente durante las pruebas.

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
mysqladmin -u $IA2_MAIN_DB_ROOT_PASS -p create $IA2_MAIN_DB_NAME
mysqladmin -u $IA2_DB_DATA_ROOT_PASS -p create $IA2_DB_DATA_NAME
```

### Ambiente de desarrollo utilizando Docker

Before running the system for the first time, and any time you make changes in the `tasks.py` file, you'll have to run:

Utilizamos el siguiente comando para construír la imagen de Docker con todas las dependencias necesarias.

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

Es posible correr las migraciones utilizando el siguiente comando:

```bash
docker-compose exec web make django-migrate
```

Cada vez que realice cambios de internacionalización, será necesario re-compilar los archivos `.po` con el siguiente comando.

```bash
docker-compose exec web make django-compile-messages
```

Si desea inicializar una shell interactiva de Python puede realizarlo utilizando el siguiente comando:

```bash
docker-compose exec web python manage.py shell
```

Si realiza cambios en cualquiera de los fixture, puede inicializarlos con el siguiente comando:

```bash
docker-compose exec web make django-load-fixtures
```

Si desea crear un superuser de Django, puede realizarlo de la siguiente manera:

```bash
# Inicia los pasos que lo guiarán para crear un superusuario
docker-compose exec web python manage.py createsuperuser
```

### Herramientas de debugging

Es posible inciar el servidor de manera tal de poder utilizar herramientas de debugging como Wekzeug y/o PyInstrument.

+ [`Werkzeug:`](https://werkzeug.palletsprojects.com/en/0.15.x/tutorial/) Para desabilitar e PIN para debugging en ambientes locales, es necesario setear la siguiente variable de entorno en `.env`: `WERKZEUG_DEBUG_PIN=off`
+ [`PyInstrument:`](https://github.com/joerick/pyinstrument/) Es posible habilitar PyInstrument utilizando `ENABLE_PYINSTRUMENT=on` en `.env`. Los archivos html de PyInstrument se acceden desde `profiles/`.

Ejemplo utilizando Docker:

```bash
docker-compose exec web WERKZEUG_DEBUG_PIN=off ENABLE_PYINSTRUMENT=on python manage.py runserver_plus
```

## Flujo de desarrollo

### Agregar nuevas dependencias

Se pueden agregar nuevos paquetes utilizando `pip` dentro del container

```bash
docker-compose exec web pip install <package_name>
```

Cada vez que instalamos un paquete, **debemos** obtener el *freeze* de las versiones.

```bash
docker-compose exec web pip freeze | grep <package_name>
```

Inclúya la dependencia en el archivo *requirements* que corresponda. Existen 4 tipos de archivos de *requirements*:

+ `base.txt`: dependencias utilizadas en todos los ambientes.
+ `local.txt`: dependencias utilizadas únicamente en el ambiente local de desarrollo.
+ `production.txt`: dependencias utilizadas únicamente en ambientes de producción.
+ `testing.txt`: dependencias utilizadas únicamente en ambientes de pruebas.

```bash
$ docker-compose exec web pip freeze | grep mysqlclient

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

Si la configuración del ambiente utiliza Docker, entonces los comandos sufren un ligero cambio:

```bash
docker-compose exec web make test
```

```bash
docker-compose exec web make test.wip
```

> Los comandos con Docker asumen que los servicios de docker-compose están activos.



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
