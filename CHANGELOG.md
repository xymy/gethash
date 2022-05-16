# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [5.2] - 2022-05-16

### Changed

- `HashFileReader.iter_hash` now accepts `root` argument.

### Packaging

- Removed `setup.py`. Now use `python -m build`.

## [5.1] - 2022-01-18

### Documentation

- Sphinx now uses `MyST-Parser` for writing markdown documentation.
- Added changelog to documentation.

## [5.0] - 2021-12-24

### Added

- Added backends for `Hashlib` and `PyCryptodome`.

### Removed

- Removed ``sorted_locale()`` function.
- Removed entry points for legacy commands.

### Packaging

- Switched `PyCryptodomex` dependency to `PyCryptodome` dependency.
- Added PyPI classifier `Intended Audience :: Developers`.

[Unreleased]: https://github.com/xymy/gethash/compare/v5.2...HEAD
[5.2]: https://github.com/xymy/gethash/compare/v5.1...v5.2
[5.1]: https://github.com/xymy/gethash/compare/v5.0...v5.1
[5.0]: https://github.com/xymy/gethash/compare/v4.9...v5.0
