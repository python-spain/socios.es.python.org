Usuarios
========

Solicitar restauración de contraseña
------------------------------------

Para inicializar el proceso de restaurar la contraseña de un usuario, se tiene que
realizar una llamada al API para solicitar un envío de un código de restauración.

.. http:post:: /api/v1/request_restore_code/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST /api/v1/request_restore_code/ HTTP/1.1
        Content-Type: application/json

        {
            "email": "user@example.com"
        }


    **Ejemplo de respuesta**:

    .. sourcecode:: http

        HTTP/1.1 201 Created

Al completarse la llamada correctamente, el usuario recibirá un correo electrónico con
un enlace donde, al entrar, se le solicitará una nueva contraseña. Este enlace podrá
llevar a dos tipos de páginas:

* Integrada con el *frontend*, que hará uso de un API para restaurar la contraseña,
* Página interna, directamente renderizada y gestionada por el backend, que se encargará de mostrar el formulario para el cambio de contraseña

El enlace del correo puede llegar como se necesite desde el punto de vista del
frontend o de la página interna, pero en general tendrá un aspecto similar a::

    https://{ domain }/users/restore-password/{restore_password_code }/


Restaurar la contraseña
-----------------------

Si se usa el API para restaurar la contraseña desde una página del *frontend*, se
tendrá que obtener el código de restauración de la URL y realizar la siguiente
petición:

.. http:post:: /api/v1/restore_password/

    **Ejemplo de petición**:

    .. sourcecode:: http

        POST /api/v1/restore_password/ HTTP/1.1
        Content-Type: application/json

        {
            "password": "new_password",
            "repeat_password": "new_password",
            "restore_password_code": "{restore_password_code}"
        }


    **Ejemplo de respuesta**:

    .. sourcecode:: http

        HTTP/1.1 201 Created
