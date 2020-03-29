.. Python Spain documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Docimentación de Python Spain
================================================

Documentación extendida de **Python Spain**. Puedes encontrar la documentación
generada automáticamente en:

* `Documentación automática </api/v1/docs/>`_

.. warning::

    La documentación automática requiere estar autenticado en el panel de
    administración, y solo muestra **las acciones que el usuario autenticado puede realizar**.


.. note::

    Recordad que **todas** las llamadas al API han de acabar en ``/``, ya que el
    servidor responde con una redirección cuando no se añade, añadiéndola, y si no
    se lleva cuidado, el cliente puede gestionarla como un ``GET`` perdiendo así
    lo que se haya enviado en caso de que la original fuera un ``POST``, un ``PUT``
    o un ``PATCH``.

.. toctree::
    :caption: Visión General
    :maxdepth: 2
    :glob:

    overview/*

.. toctree::
    :caption: Referencia
    :maxdepth: 2

    reference/auth
    reference/api
