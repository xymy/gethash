# Gethash

[![PyPI](https://img.shields.io/pypi/v/gethash)](https://pypi.org/project/gethash/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gethash)](https://pypi.org/project/gethash/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/gethash)](https://pypi.org/project/gethash/)
[![PyPI - License](https://img.shields.io/pypi/l/gethash)](https://pypi.org/project/gethash/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Gethash is a command-line hash utility.

## Installation

```shell
$ pip install -U gethash
```

or (if you need legacy hash algorithms)

```shell
$ pip install -U "gethash[all]"
```

*Note: Gethash requires Python 3.7 and later.*

## Usage

After installation, 9 commands are available:

- crc32
- md5
- sha1
- sha256
- sha512
- sha3-256
- sha3-512
- blake2b
- blake2s

If you use `[all]`, 3 additional commands are available:

- md2
- md4
- ripemd160

### Generate hash values

```shell
$ ls -l
total 296
-rw-r--r-- 1 User 197610  68074 Jun 27 10:43 001.zip
-rw-r--r-- 1 User 197610 126717 Jun 27 10:43 002.zip
-rw-r--r-- 1 User 197610 103064 Jun 27 10:44 003.zip

$ sha1 -s *.zip
7701133eb84b567362fbf1b9e3883d7620ee8ada *001.zip
0d6c6cb6908064139f419c1b528f99142a1f2a49 *002.zip
10e2c0d8aa85add2ba495393f7f7f0b0baaf34a6 *003.zip

$ ls -l
total 299
-rw-r--r-- 1 User 197610  68074 Jun 27 10:43 001.zip
-rw-r--r-- 1 User 197610     51 Jun 27 10:44 001.zip.sha1
-rw-r--r-- 1 User 197610 126717 Jun 27 10:43 002.zip
-rw-r--r-- 1 User 197610     51 Jun 27 10:44 002.zip.sha1
-rw-r--r-- 1 User 197610 103064 Jun 27 10:44 003.zip
-rw-r--r-- 1 User 197610     51 Jun 27 10:44 003.zip.sha1
```

### Check hash values

```shell
$ cat *.sha1
7701133eb84b567362fbf1b9e3883d7620ee8ada *001.zip
0d6c6cb6908064139f419c1b528f99142a1f2a49 *002.zip
10e2c0d8aa85add2ba495393f7f7f0b0baaf34a6 *003.zip

$ sha1 -c *.sha1
[SUCCESS] 001.zip
[SUCCESS] 002.zip
[SUCCESS] 003.zip
```

## Project Links

- Home Page: https://github.com/xymy/gethash
- PyPI Release: https://pypi.org/project/gethash/
- Documentation: https://github.com/xymy/gethash
- Issue Tracker: https://github.com/xymy/gethash/issues
- Source Code: https://github.com/xymy/gethash
