# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project (mostly) adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Documentation

## ## 0.0.4 - 2024-03-26

### Added

    - Hostname methods
      `upper()`, `lower()`, `title()`, and `capitalize()`,
      which preserve hostnameness.

### Changed

    - Bad flags or flag values result in `TypeError`
    - `InvalidCharacter` exception renamed to `BadCharacterError`.
    - Removed misuse of `Self`
    - Minimum python version is 3.10 instead of 3.11.
    - Addressed `ruff.toml` deprecations.

### Documentation

    - Improved type checking examples

    - Expanded documentation for exception handling.

    - Fixed some doctests hadn't really been testing testing.

## 0.0.3 - 2024-02-24

### Added

    - (Partial) documentation about relevant Internet standards

### Changed

    - `Hostname.labels()` is now how to get labels.

## 0.0.2 - 2024-02-22

### Added

    - py.typed
    - Changelog
    - Sphinx documentation

### Changed

    - Removed `name` name space.
    - Removed `Name` class and combined its functionality with `Hostname` class

## 0.0.1 - 2024-01-27

Not meant for public consumption

### Added

    - The whole kit and caboodle
