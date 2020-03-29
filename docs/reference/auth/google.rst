Autenticación con Google
========================

El sistema asume que de forma externa a este se obtiene un access token válido
para usar el API de **Google OAuth2**. Una vez obtenido este token, para poder usar la
aplicación, se tiene que realizar una conversión a un token propio.

Para hacer esto se tiene que hacer la siguiente llamada, usando los credenciales
que se obtienen en :ref:`Autenticación vía OAuth <oauth>`:


.. http:post:: /api/v1/auth/oauth/token/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST /api/v1/auth/oauth/convert-token/ HTTP/1.1
        Content-Type: application/json

        {
            "grant_type": "convert_token",
            "client_id": "...",
            "client_secret": "...",
            "backend": "google-oauth2",
            "token": "<backend token>"
        }

