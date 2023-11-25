# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Now `--sync` option supports nanoseconds timestamp without precision loss.

### Removed

- Removed `PathWithSuffix` class.

### Documentation

- Added `--no-clean` and `--no-dist` options to `docs/release.py` script.

### Linting

- Adopted more `ruff` rules.

### Testing

- Improved tox config.
- Now store `hypothesis` and `pytest` cache in `.cache` directory.

## [6.0] - 2023-11-19

### Added

- Added `AggOutput`, `SepOutput` and `NullOutput` classes.

### Changed

- Changed `Output` to abstract base class.
- Refactored `CRC32` class.
- Now `CheckHashLineError` requires hexadecimal hash value string.
- Refactored `format_hash_line()` and `parse_hash_line()`.

### Configuration

- Added Python 3.12 support.
- Dropped Python 3.8 support.

### Documentation

- Updated project links.

### Linting

- Adopted `check-case-conflict` and `check-merge-conflict` for `pre-commit-hooks`.
- Updated `mymy` configuration.
- Now store `ruff` and `mypy` cache in `.cache` directory.

### Testing

- Added test cases for `gethash.wrappers.crc32`.
- Added more test data.
- Adopted `more-itertools` for testing.
- Improved tox config.

## [5.9] - 2023-10-30

### Changed

- Now `Hasher` supports `pathlib.Path`.
- Now `HashFileReader` and `HashFileWriter` support `pathlib.Path`.
- Now `format_hash_line()`, `parse_hash_line()`, `generate_hash_line()` and `check_hash_line()` support `pathlib.Path`.

### Configuration

- Migrated build system from `setuptools` to `hatch`.
- Now use `hatch` to setup development environment.

### Documentation

- Improved documentation.
- Improved changelog.

## [5.8] - 2023-10-24

### Configuration

- Now allow to setup development environment via `tox devenv -e dev .venv`.

### Documentation

- Migrated documentation dependencies to `setup.cfg`.
- Updated `docs/release.py` script.
- Updated `docs/source/conf.py`.
- Refactored root doc from `index.rst` to `index.md`.
- Added `pre-commit` and `ruff` badges to documentation.
- Removed `isort` badge from documentation.
- Changed title for HTML documentation to `{project} {release}`.
- Improved changelog.

### Testing

- Now require `tox>=4.4`.
- Fixed and improved configuration for `tox`.
- Added exclude lines for `coverage`.
- Added more test cases.

## [5.7] - 2023-10-21

### Configuration

- Migrated development dependencies to `setup.cfg`.

### Linting

- Now require `pre-commit>=3.0`.
- Adopted `ruff`.
- Removed `isort`, `flake8` and `yesqa`.

## [5.6] - 2022-10-19

### Configuration

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
- Added `gethash.backends` entry points.

### Changed

- Changed type annotation of `ctx` argument from `Any` to `HashContext`.
- Now load backends via entry points.

### Configuration

- Added Python 3.11 support.

### Linting

- Adopted `flake8-comprehensions` and `flake8-simplify`.
- Migrated `mypy` configuration to `pyproject.toml`.

## [5.3] - 2022-06-05

### Changed

- Changed type annotations for `Hasher.__init__()`.
- Renamed argument of `Hasher.__init__()` from `tqdm_class` to `tqdm_type`.
- `--start` and `--stop` options now require non-negative integers.

### Fixed

- Fixed a reading error when `chunksize < 0` for `Hasher._hash_file()`.

### Configuration

- Dropped Python 3.7 support.

### Linting

- Adopted `pre-commit` for running linters automatically.
- Adopted `flake8-bugbear` and `flake8-implicit-str-concat`.

## [5.2] - 2022-05-16

### Added

- Added `root` argument to `HashFileReader.iter_hash()`.

### Configuration

- Removed `setup.py`. Now use `python -m build`.

## [5.1] - 2022-01-18

### Documentation

- Adopted `myst-parser` for writing Markdown documentation.
- Added changelog to documentation.

## [5.0] - 2021-12-24

### Added

- Added backends for `hashlib` and `pycryptodome`.

### Removed

- Removed `sorted_locale()` function.
- Removed entry points for legacy commands.

### Configuration

- Switched dependency from `pycryptodomex` to `pycryptodome`.
- Added PyPI classifier `Intended Audience :: Developers`.

[Unreleased]: https://github.com/xymy/gethash/compare/v6.0...HEAD
[6.0]: https://github.com/xymy/gethash/compare/v5.9...v6.0
[5.9]: https://github.com/xymy/gethash/compare/v5.8...v5.9
[5.8]: https://github.com/xymy/gethash/compare/v5.7...v5.8
[5.7]: https://github.com/xymy/gethash/compare/v5.6...v5.7
[5.6]: https://github.com/xymy/gethash/compare/v5.5...v5.6
[5.5]: https://github.com/xymy/gethash/compare/v5.4...v5.5
[5.4]: https://github.com/xymy/gethash/compare/v5.3...v5.4
[5.3]: https://github.com/xymy/gethash/compare/v5.2...v5.3
[5.2]: https://github.com/xymy/gethash/compare/v5.1...v5.2
[5.1]: https://github.com/xymy/gethash/compare/v5.0...v5.1
[5.0]: https://github.com/xymy/gethash/compare/v4.9...v5.0
