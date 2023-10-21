# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Linting

- Removed `isort`, `flake8` and `yesqa`.

## [5.6] - 2022-10-19

### Dependencies

- Migrated development dependencies to `requirements-dev.txt`.

### Documentation

- Added `docs/release.py` script for building documentation.
- Improved documentation.

### Linting

- Adopted `yesqa`.

### Testing

- Adopted `coverage`, `pytest`, `pytest-cov` and `tox` for testing.

## [5.5] - 2022-07-17

### Added

- Added `gethash.wrappers` package.
- Added `WrappersBackend` class for loading commands from `gethash.wrappers`.

### Changed

- Moved `crc32` module from `gethash.utils` to `gethash.wrappers`.
- Improved type annotations.

### Linting

- Adopted `pyupgrade`.

## [5.4] - 2022-06-24

### Added

- Added `HashContext` protocol class for annotating hash context type.

### Changed

- Changed type annotation of `ctx` argument from `Any` to `HashContext`.
- Now load backends via entry points.

### Linting

- Adopted `flake8-comprehensions` and `flake8-simplify`.
- Migrated `mypy` configuration to `pyproject.toml`.

### Packaging

- Added `gethash.backends` entry points.

## [5.3] - 2022-06-05

### Changed

- Changed type annotations for `Hasher.__init__()`.
- Renamed argument of `Hasher.__init__()` from `tqdm_class` to `tqdm_type`.
- `--start` and `--stop` options now require non-negative integers.

### Fixed

- Fixed a reading error when `chunksize < 0` for `Hasher._hash_file()`.

### Dependencies

- Dropped Python 3.7 support.

### Linting

- Adopted `pre-commit` for running linters automatically.
- Adopted `flake8-bugbear` and `flake8-implicit-str-concat`.

## [5.2] - 2022-05-16

### Changed

- `HashFileReader.iter_hash()` now accepts `root` argument.

### Packaging

- Removed `setup.py`. Now use `python -m build`.

## [5.1] - 2022-01-18

### Documentation

- Adopted `myst-parser` for writing Markdown documentation.
- Added changelog to documentation.

## [5.0] - 2021-12-24

### Added

- Added backends for `hashlib` and `pycryptodome`.

### Removed

- Removed ``sorted_locale()`` function.
- Removed entry points for legacy commands.

### Dependencies

- Switched dependency from `pycryptodomex` to `pycryptodome`.

### Packaging

- Added PyPI classifier `Intended Audience :: Developers`.

[Unreleased]: https://github.com/xymy/gethash/compare/v5.6...HEAD
[5.6]: https://github.com/xymy/gethash/compare/v5.5...v5.6
[5.5]: https://github.com/xymy/gethash/compare/v5.4...v5.5
[5.4]: https://github.com/xymy/gethash/compare/v5.3...v5.4
[5.3]: https://github.com/xymy/gethash/compare/v5.2...v5.3
[5.2]: https://github.com/xymy/gethash/compare/v5.1...v5.2
[5.1]: https://github.com/xymy/gethash/compare/v5.0...v5.1
[5.0]: https://github.com/xymy/gethash/compare/v4.9...v5.0
