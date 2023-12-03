# Notas

## Comandos

```bash
pip install Django==4.2.7 # Instalar Django en una version especifica

# Crear un proyecto
django-admin startproject mysite

# Crear una app
python manage.py startapp polls

```

## Configuracion

- Debo agregar cualquier app que cree (en este caso app) en el archivo settings.py en la variable INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ...
    'app', # Agrego la app que cree
]
```

- Debo agregar la ruta de la app en el archivo urls.py del proyecto

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('app/', include('app.urls')), # Agrego la ruta de la app
    path('admin/', admin.site.urls),
]
```

## Base de datos

- En este caso el profe utiliza MySQL pero yo utilizaré PostgreSQL

- Instalar el paquete de PostgreSQL

```bash
pip install psycopg2
```

- Configurar la base de datos en el archivo settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cac_movies_24',
        'USER': 'emi',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```

- APPEND_SLASH: Si esta en True, Django agrega una barra al final de la url. Si esta en False, Django no agrega la barra al final de la url. Por defecto esta en True.

```python
APPEND_SLASH = False
```

## Variables de entorno

- Parquete: django-environ

```bash
pip install django-environ
```

- Creamos un archivo .env en la raiz del proyecto (en este caso la carpeta cac_movies_bkn_24). Sería donde está el archivo settings.py. Este archivo no se sube a github ya que contiene informacion sensible.

- El archivo .env tendria lo siguiente:

```bash
SECRET_KEY = django-insecure-#_zsnlupucpxip&#h$)=%(0+)6t156#uw%n0(+1340pg(nkkt9

DATABASE_ENGINE: django.db.backends.postgresql_psycopg2,
DATABASE_NAME: cac_movies_24,
DATABASE_USER: emi,
DATABASE_PASSWORD: admin,
DATABASE_HOST: localhost,
DATABASE_PORT: 5432,
```

- En el archivo settings.py importamos el paquete y lo utilizamos para obtener las variables de entorno

```python
import os
import environ

env = environ.Env()
environ.Env.read_env() # reading .env file

SECRET_KEY = env('SECRET_KEY')

```

### Migraciones

- Las migraciones son como los commits de git. Son los cambios que se van haciendo en la base de datos. Instrucciones que se van guardando para que la base de datos sepa como tiene que estar.

- Para crear una migracion:

```bash
python manage.py makemigrations
```

- Para aplicar las migraciones:

```bash
python manage.py migrate
```

- Para ver el sql que se va a ejecutar:

```bash
python manage.py sqlmigrate app 0001
```

#### Flujo de migraciones

- Creamos un modelo en models.py
- Creamos una migracion con makemigrations
  - Este comando crea un archivo en la carpeta migrations de la app indicando los cambios que se van a hacer en la base de datos. Genera un archivo con un numero de version. En este caso 0001
- Aplicamos la migracion con migrate
  - Este comando ejecuta el archivo de migracion que se genero en la carpeta migrations de la app. En este caso 0001
- Cada modificación que hagamos en el modelo, se debe crear una migracion y aplicarla con makemigrations y migrate. Se genera un historial de cambios en los modelos de la base de datos.

## Subir archivos

- En models.py utilizamos el campo ImageField para subir archivos

```python
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/') # Campo para subir archivos. Donde indica el parametro upload_to es la carpeta donde se van a guardar los archivos

    def __str__(self):
        return self.title
```

- Debemos utilizar la libreria Pillow para poder subir archivos

```bash
pip install Pillow
```

Debemos configurar la carpeta donde se van a guardar los archivos en el archivo settings.py

```python
MEDIA_URL = '/media/' # URL donde se van a guardar los archivos

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Carpeta donde se van a guardar los archivos
```

### Mostrar archivos

- En el archivo urls.py del proyecto debemos agregar la siguiente linea para que se puedan mostrar los archivos

```python
from django.contrib import admin

from django.urls import include, path

from django.conf import settings # Importamos settings

from django.conf.urls.static import static # Importamos static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## API REST con Django

- Paquete: djangorestframework

```bash
pip install djangorestframework
```

- Una vez instalado el paquete, debemos agregarlo en la variable INSTALLED_APPS del archivo settings.py

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
]
```

- En el archivo urls.py del proyecto debemos agregar la siguiente linea para que se puedan mostrar los archivos

```python

urlpatterns = [
    # ...
    path('api-auth/', include('rest_framework.urls')), # Agregamos esta linea
]
```

## Serializacion

- La serializacion es el proceso de convertir un objeto en un formato que se pueda almacenar o transmitir. En este caso, convertimos los objetos de la base de datos en un formato JSON para poder enviarlos a traves de una API.

- En el archivo serializers.py de la app creamos una clase que herede de serializers.ModelSerializer

```python
from rest_framework import serializers

from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
```

## Endpoints de la API

- Vamos a utilizar @api_view para crear los endpoints de la API

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer

@api_view(['GET']) # Indicamos que el endpoint solo acepta peticiones GET
def movie_list(request):
    movies = Movie.objects.all() # Obtenemos todas las peliculas de la base de datos
    serializer = MovieSerializer(movies, many=True) # Serializamos las peliculas
    return Response(serializer.data) # Retornamos las peliculas serializadas

```

- En el archivo urls.py de la app creamos la ruta del endpoint

```python
from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.movie_list), # Creamos la ruta del endpoint
]
```

## MySQL

Mira puedes probar con lo siguiente:

Instalando esta herramienta https://visualstudio.microsoft.com/es/visual-cpp-build-tools/

y luego abriendo y cerrando visual studio code y ejecutar el comando pip install mysql nuevamante

o bien probar de instalar lo siguiente

pip install mysql-connector-python

Referencia: https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html

Avisame si te funciono alguna de las dos opciones.

## Configuración CORS

- Paquete: django-cors-headers

```bash
pip install django-cors-headers
```

- En el archivo settings.py del proyecto agregamos el paquete en la variable INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]
```

- En el archivo settings.py del proyecto agregamos el paquete en la variable MIDDLEWARE

```python
MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware', # Agregamos esta linea
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

- En el archivo settings.py del proyecto agregamos la siguiente variable

```python
CORS_ORIGIN_ALLOW_ALL = True
```
