Entorno de desarrollo
=====================

Para el desarrollo en este proyecto se asume que se tienen instalado y funcionando 
en local:

* Python 3.7 o superior
* poetry
* Docker
* docker-compose

Configuración en local
----------------------

Primero creamos un fichero ``.env`` de variables de entorno para definit el 
entorno local, por ejemplo:

.. code-block::

    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=pythonspain
    POSTGRES_USER=RfDG8JrYqyuHU5uSKneQgtAL
    POSTGRES_PASSWORD=yJwV9HsVW29jArgxEFYepBEtavz2HEtfXKyPBCthX5VvzbsN

    # General
    # ------------------------------------------------------------------------------
    USE_DOCKER=no

    # Django
    # ------------------------------------------------------------------------------
    DJANGO_SECRET_KEY=PBu5GeHqMGS2snMgmZx2uAbc

    # Redis
    # ------------------------------------------------------------------------------
    REDIS_URL=redis://redis:6379/0

    # Celery
    # ------------------------------------------------------------------------------
    CELERY_BROKER_URL=redis://redis:6379/0

    # Database connection
    # ------------------------------------------------------------------------------
    DATABASE_URL=postgres://RfDG8JrYqyuHU5uSKneQgtAL:yJwV9HsVW29jArgxEFYepBEtavz2HEtfXKyPBCthX5VvzbsN@localhost:5432/pythonspain

El proyecto está configurado con ``poetry``, así que podemos crear el entorno virutal 
simplemente con:

.. code-block:: console

    $ poetry install

Por último lanzamos los servicios locales con docker-compose:

.. code-block:: console

    $ docker-compose -f local.yml up --build

Tests
-----

Para ejecutar los tests:

.. code-block:: console

    $ poetry run pytest .


Servidor local
--------------

Para ejecutar el servidor local:

.. code-block:: console

    $ poetry run ./manage.py runserver