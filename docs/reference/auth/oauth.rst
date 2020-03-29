.. _oauth:

Autenticación vía OAuth
=======================

El sistema soporta por defecto autenticación usando el protocolo **OAuth 2.0**.

Para hacer uso de esta autenticación, primero se ha de crear una **aplicación**,
que puede ser creada desde el `panel de administración </admin/oauth2_provider/application/>`_.


Crear aplicación
----------------

Si no está creada la aplicación, crearemos una nueva, teniendo en cuenta que:

* El campo ``client type`` tendrá el valor de ``Confidential``.
* El campo ``authorization grant type`` tendrá el valor de de ``Resource owner password-based``.

Una vez creado, nos quedaremos con los valores de ``client id`` y ``client secret`` que
el backend habrá generado automáticamente.


Obtener un access token
-----------------------

Podemos obtener un access token válido para autenticar las llamadas haciendo la
siguiente petición:

.. http:post:: /api/v1/auth/oauth/token/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST /api/v1/auth/oauth/token/ HTTP/1.1
        Content-Type: application/json
        Authorization: Basic S2Q4U1RUc055Y2RYZEtXSHFXOVMyY1JpZXVCVTRLeW4yUDRydTRJeTpadnNlZGwxaDkxbkUzd3Qza2RmRUsxRjRnVUhZeDc5V0N1OXduUUR5ZlB1Skpqem9BbmpOR01VQ0JJZUZEN1RRNmVTbFQyT1pUeUNJbTZoMjZ6c2NCSUM2SzJhaHA2U2FRZENrbUs0d015dUNRb0Vvb1RZVjdoUzZVbXFxQlUwMg

        {
            "grant_type": "password",
            "username": "email@example.com",
            "password": "password",
        }


    **Ejemplo de respuesta**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "access_token": "IURMeAXBxcOpm82B9xvUuITTexgY3z",
            "expires_in": 36000,
            "token_type": "Bearer",
            "scope": "read write",
            "refresh_token": "EJX1gyc6sSYQk7HBdLubULX6uGgzaM"
        }

La cabecera ``Authorization`` tiene el resultado de aplicar la codificación en
**base 64** a la cadena ``{client id}:{client secret}``, donde ``{client id}`` se
corresponde con la cadena ``client id`` obtenida en la creación de la aplicación y
``{client secret}`` a la cadena ``client secret`` obtenida  también en la creación
de la aplicación.

Refrescar un access token
-------------------------

Usando el campo ``refresh_token`` de la respuesta de la petición anterior, se puede
refrescar el token de la siguiente manera:


.. http:post:: /api/v1/auth/oauth/token/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST /api/v1/auth/oauth/token/ HTTP/1.1
        Content-Type: application/json
        Authorization: Basic S2Q4U1RUc055Y2RYZEtXSHFXOVMyY1JpZXVCVTRLeW4yUDRydTRJeTpadnNlZGwxaDkxbkUzd3Qza2RmRUsxRjRnVUhZeDc5V0N1OXduUUR5ZlB1Skpqem9BbmpOR01VQ0JJZUZEN1RRNmVTbFQyT1pUeUNJbTZoMjZ6c2NCSUM2SzJhaHA2U2FRZENrbUs0d015dUNRb0Vvb1RZVjdoUzZVbXFxQlUwMg

        {
            "grant_type": "refresh_token",
            "refresh_token": "EJX1gyc6sSYQk7HBdLubULX6uGgzaM",
        }


    **Ejemplo de respuesta**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "access_token": "18xGgi3bQG4yArnP9sAEgr6pubqh2K",
            "expires_in": 36000,
            "token_type": "Bearer",
            "scope": "read write",
            "refresh_token": "sHIMWkToz2rwjpVIE4hrd7g2EaVGbE"
        }


Realizar una petición con autenticación
----------------------------------------

Una vez obtenido el token, se puede usar para hacer una petición al API que requiera
autenticación. Por ejemplo:

.. http:get:: /api/v1/users/me/

    **Ejemplo de petición**:

    .. sourcecode:: http

        GET /api/v1/users/me/ HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer 18xGgi3bQG4yArnP9sAEgr6pubqh2K
