Autenticación vía JWT
=====================

El sistema soporta por defecto autenticación usando el protocolo **JWT (JSON Web Token Authentication)**.

Obtener un token
----------------

Podemos obtener un token válido para autenticar las llamadas haciendo la
siguiente petición:

.. http:post:: /api/v1/auth/jwt/token/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST /api/v1/auth/jwt/token/ HTTP/1.1
        Content-Type: application/json

        {
            "email": "email@example.com",
            "password": "password",
        }


    **Ejemplo de respuesta**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InJ3aGl0ZUBob3RtYWlsLmNvbSIsImV4cCI6MTU2Njg0NjE1MiwiZW1haWwiOiJyd2hpdGVAaG90bWFpbC5jb20iLCJvcmlnX2lhdCI6MTU2Njg0MjU1Mn0.ta3rK76Y6Jtlfo7twzfwVrFDmkY_p10Id3FEReKWgnI"
        }


Refrescar un token
------------------

Un JWT puede ser renovado, usando la siguiente llamada:

.. http:post:: /api/v1/auth/jwt/refresh/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST "/api/v1/auth/jwt/refresh/ HTTP/1.1
        Content-Type: application/json

        {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InJ3aGl0ZUBob3RtYWlsLmNvbSIsImV4cCI6MTU2Njg0NjE1MiwiZW1haWwiOiJyd2hpdGVAaG90bWFpbC5jb20iLCJvcmlnX2lhdCI6MTU2Njg0MjU1Mn0.ta3rK76Y6Jtlfo7twzfwVrFDmkY_p10Id3FEReKWgnI"
        }


    **Ejemplo de respuesta**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NiwidXNlcm5hbWUiOiJqc3Rld2FydEBjb2hlbi5jb20iLCJleHAiOjE1NjY4NDYzOTcsImVtYWlsIjoianN0ZXdhcnRAY29oZW4uY29tIiwib3JpZ19pYXQiOjE1NjY4NDI3OTd9.yRdL4QCFIn0FvpaNS2_0VvfQr0MRyv9FcmafAWA7QO4"
        }
