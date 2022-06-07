=====================
Gethash Documentation
=====================

.. image:: https://img.shields.io/pypi/v/gethash
    :target: https://pypi.org/project/gethash/

.. image:: https://img.shields.io/pypi/pyversions/gethash
    :target: https://pypi.org/project/gethash/

.. image:: https://pepy.tech/badge/gethash/month
    :target: https://pepy.tech/project/gethash

.. image:: https://img.shields.io/pypi/l/gethash
    :target: https://pypi.org/project/gethash/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/

Gethash is a command-line hash utility.

Installation
------------

Install from PyPI:

.. code-block:: shell

    $ pip install gethash

or if you need legacy hash algorithms:

.. code-block:: shell

    $ pip install "gethash[all]"

.. note::

    Gethash requires Python 3.8 and later.

Usage
-----

After installation, 10 commands are available:

- crc32
- md5
- sha1
- sha256
- sha512
- sha3-256
- sha3-512
- blake2b
- blake2s
- gethash

Show command-line usage:

.. code-block:: shell

    $ gethash --help
    Usage: gethash [OPTIONS] COMMAND [ARGS]...

    Generate or check various hash values.

    Options:
    -V, --version  Show the version and exit.
    -h, --help     Show this message and exit.

    Commands:
    blake2b     Generate or check BLAKE2b.
    blake2s     Generate or check BLAKE2s.
    crc32       Generate or check CRC32.
    md2         Generate or check MD2.
    md4         Generate or check MD4.
    md5         Generate or check MD5.
    md5-sha1    Generate or check MD5-SHA1.
    mdc2        Generate or check MDC2.
    ripemd160   Generate or check RIPEMD160.
    sha1        Generate or check SHA1.
    sha3-224    Generate or check SHA3-224.
    sha3-256    Generate or check SHA3-256.
    sha3-384    Generate or check SHA3-384.
    sha3-512    Generate or check SHA3-512.
    sha224      Generate or check SHA224.
    sha256      Generate or check SHA256.
    sha384      Generate or check SHA384.
    sha512      Generate or check SHA512.
    sha512-224  Generate or check SHA512-224.
    sha512-256  Generate or check SHA512-256.
    sm3         Generate or check SM3.
    whirlpool   Generate or check WHIRLPOOL.

Project Links
-------------

- Home Page: https://github.com/xymy/gethash
- PyPI Release: https://pypi.org/project/gethash/
- Documentation: https://github.com/xymy/gethash
- Issue Tracker: https://github.com/xymy/gethash/issues
- Source Code: https://github.com/xymy/gethash

Table of Contents
-----------------

.. toctree::
    :maxdepth: 2

    api/index
    changelog
