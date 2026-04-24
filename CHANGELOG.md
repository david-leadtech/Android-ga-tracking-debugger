# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

## [1.0.0] - 2026-04-24

First tagged release for this maintained fork (`david-leadtech/Android-ga-tracking-debugger`).

### Added

- Pytest coverage for `log_parser` and GitHub Actions CI (Ubuntu, macOS, Windows; Python 3.9 and 3.12).
- `requirements-dev.txt` and README instructions for local tests.
- Device selection when multiple devices are connected (`adb -s <serial>` for logcat and related ADB calls).
- Status strip for ADB / device / capture state; `last_device_serial` persisted in config.
- Export session to JSON (events, user properties, consent history, device serial, app version).
- Double-click on tree rows for event, user property, and consent details.
- Keyboard shortcut to focus search (Ctrl+F / Cmd+F).
- `ttk` theme selection by platform (aqua / vista / clam).
- Parser support for `Setting user property (FE):` log line variant.
- Changelog, release workflow on `v*.*.*` tags, and repository docs for this fork.

### Fixed

- Top-level menu `entryconfig` indices for dynamic language labels.
