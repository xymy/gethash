Core
====

.. currentmodule:: gethash.core

Functions
---------

.. autofunction:: format_hash_line

.. autofunction:: parse_hash_line

.. autofunction:: generate_hash_line

.. autofunction:: check_hash_line

Classes
-------

Hasher
~~~~~~

.. autoclass:: Hasher

.. automethod:: Hasher.__call__

.. automethod:: Hasher.hash

.. automethod:: Hasher.hash_file

.. automethod:: Hasher.hash_dir

HashFileReader
~~~~~~~~~~~~~~

.. autoclass:: HashFileReader

.. automethod:: HashFileReader.read_hash_line

HashFileWriter
~~~~~~~~~~~~~~

.. autoclass:: HashFileWriter

.. automethod:: HashFileWriter.write_hash_line

Exceptions
----------

.. autoexception:: IsADirectory

.. autoexception:: ParseHashLineError

.. autoexception:: CheckHashLineError
