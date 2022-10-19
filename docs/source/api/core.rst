gethash.core
============

.. currentmodule:: gethash.core

Functions
---------

.. autofunction:: format_hash_line

.. autofunction:: parse_hash_line

.. autofunction:: generate_hash_line

.. autofunction:: check_hash_line

.. autofunction:: re_name_to_hash

.. autofunction:: re_hash_to_name

Classes
-------

HashFileReader
~~~~~~~~~~~~~~

.. autoclass:: HashFileReader
    :members:
    :show-inheritance:

.. note::

    :meth:`Hasher.__iter__` is an alias of :meth:`HashFileReader.iter`.

HashFileWriter
~~~~~~~~~~~~~~

.. autoclass:: HashFileWriter
    :members:
    :show-inheritance:

Exceptions
----------

.. autoexception:: ParseHashLineError

.. autoexception:: CheckHashLineError
