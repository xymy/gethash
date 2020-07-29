# gethash

A command-line tools that can generate or check hash values.

## Installation

Require Python 3.6+.

```shell
pip install -U gethash
```

or

```shell
pip3 install -U gethash
```

## Usage

After installation, 6 commands are available:

- md5
- sha1
- sha256
- sha512
- blake2b
- blake2s

```shell
$ ls -l
total 296
-rw-r--r-- 1 User 197610  68074 Jun 27 10:43 001.zip
-rw-r--r-- 1 User 197610 126717 Jun 27 10:43 002.zip
-rw-r--r-- 1 User 197610 103064 Jun 27 10:44 003.zip

$ sha1 *.zip
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

$ cat *.sha1
7701133eb84b567362fbf1b9e3883d7620ee8ada *001.zip
0d6c6cb6908064139f419c1b528f99142a1f2a49 *002.zip
10e2c0d8aa85add2ba495393f7f7f0b0baaf34a6 *003.zip

$ sha1 -c *.sha1
[SUCCESS] 001.zip
[SUCCESS] 002.zip
[SUCCESS] 003.zip
```
