Backups de base de datos
========================

Existen una serie de comandos para la gestión de los backups de la base de 
datos. Estos comando crean, listan y restauran volcados de la base de datos,
almacenados en un volumen específico.

Listar backups
--------------

.. code-block:: console

    $ docker-compose -f production.yml run --rm postgres backups
    These are the backups you have got:
    total 24K
    -rw-r--r-- 1 root root 24K Mar 31 23:28 backup_2020_03_31T23_28_45.sql.gz


Crear un backup nuevo
---------------------

.. code-block:: console

    $ docker-compose -f production.yml run --rm postgres backup
    Backing up the 'pythonspain' database...
    SUCCESS: 'pythonspain' database backup 'backup_2020_04_02T17_35_20.sql.gz' has been created and placed in '/backups'.

Restaurar un backup
-------------------


.. code-block:: console

    $ docker-compose -f production.yml run --rm restore backup_2020_04_02T17_35_20.sql.gz
