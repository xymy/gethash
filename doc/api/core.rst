Core
====

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

Hasher
~~~~~~

.. autoclass:: Hasher

.. automethod:: Hasher.hash

.. note::

    :meth:`Hasher.__call__` is an alias of :meth:`Hasher.hash`.

.. automethod:: Hasher.hash_file

.. automethod:: Hasher.hash_dir

HashFileReader
~~~~~~~~~~~~~~

.. autoclass:: HashFileReader

.. automethod:: HashFileReader.read_hash_line

.. automethod:: HashFileReader.iter

.. note::

    :meth:`Hasher.__iter__` is an alias of :meth:`HashFileReader.iter`.

.. automethod:: HashFileReader.iter2

.. automethod:: HashFileReader.iter3

.. automethod:: HashFileReader.iter_hash

.. automethod:: HashFileReader.iter_name

.. automethod:: HashFileReader.close

HashFileWriter
~~~~~~~~~~~~~~

.. autoclass:: HashFileWriter

.. automethod:: HashFileWriter.write_hash_line

.. automethod:: HashFileWriter.write_comment

.. automethod:: HashFileWriter.close

Exceptions
----------

.. autoexception:: IsADirectory

.. autoexception:: ParseHashLineError

.. autoexception:: CheckHashLineError
