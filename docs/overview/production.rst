Entorno de producción
=====================

El proyecto está preparado para desplegarse con Docker y docker-compose y utiliza 
variables de entorno para la configuración del mismo. Para hacer un despliegue basta con 
seguir los siguientes pasos:

1. Definir variables de entorno
-------------------------------

Creamos un fichero ``.env`` en la raíz del proyecto, con un contenido como el 
siguente, cambiando los valores entre ``{}``.

.. code-block::

    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=pythonspain
    POSTGRES_USER={ usuario de base de datos }
    POSTGRES_PASSWORD={ contraseña de la base de datos }

    # Django
    # ------------------------------------------------------------------------------
    DJANGO_READ_DOT_ENV_FILE=False
    DJANGO_SECRET_KEY={ cadena de texto secreta }
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_ALLOWED_HOSTS=socios.es.python.org
    DJANGO_EMAIL_HOST={ host del servidor de correo electrónico }
    DJANGO_EMAIL_HOST_USER={ usuario para el envío de correos electrónicos }
    DJANGO_EMAIL_HOST_PASSWORD={ contraseña del usuario del correo electrónico }

    # Redis
    # ------------------------------------------------------------------------------
    REDIS_URL=redis://redis:6379/0

    # Celery
    # ------------------------------------------------------------------------------
    CELERY_BROKER_URL=redis://redis:6379/0

2. Ejecutamos los servicios con docker-compose
----------------------------------------------

.. code-block:: console

    $ docker-compose -f production.yml up -d --build

Por defecto, esto lanzará un servidor **nginx** en el puerto **5005**, que hará de proxy sobre 
la aplicación de Django.